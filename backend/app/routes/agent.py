from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select
from ..db import get_session
from ..models import AgentTask
from ..schemas import ChatIn, FormAssistIn, ApprovalIn
from ..security import require_api_key

router = APIRouter(prefix="/v1/agent", tags=["agent"], dependencies=[Depends(require_api_key)])

def last_text(result):
    messages = result.get("messages", [])
    if not messages: return "No agent message returned."
    content = getattr(messages[-1], "content", None)
    return content if isinstance(content, str) else str(content or messages[-1])

@router.post("/chat")
async def chat(data: ChatIn, request: Request):
    agent = request.app.state.agent
    if agent is None: raise HTTPException(503, "Agent not ready. Check Gemini API key and browser startup status.")
    result = await agent.ainvoke({"messages": [{"role": "user", "content": data.message}]}, config={"configurable": {"thread_id": data.thread_id}})
    return {"thread_id": data.thread_id, "response": last_text(result)}

@router.post("/form-assist")
async def form_assist(data: FormAssistIn, request: Request):
    agent = request.app.state.agent
    if agent is None: raise HTTPException(503, "Agent not ready. Check Gemini API key and browser startup status.")
    prompt = (f"Current page URL: {data.page_url}\nPage title: {data.page_title}\n"
              f"Form fields metadata: {data.fields}\nUser instruction: {data.user_instruction}\n"
              "Do not navigate or submit. Use saved profile/project vault where relevant. Return suggested field values and mark uncertain fields. "
              "Never provide passwords, OTPs, CAPTCHA answers, payment details, or legal attestations.")
    result = await agent.ainvoke({"messages": [{"role": "user", "content": prompt}]}, config={"configurable": {"thread_id": "extension-form-assist"}})
    return {"suggestions": last_text(result)}

@router.post("/tasks")
def create_task(data: ChatIn, session: Session = Depends(get_session)):
    task = AgentTask(thread_id=data.thread_id, task_type="agent", status="pending_approval", summary="Awaiting explicit user approval", payload={"message": data.message})
    session.add(task); session.commit(); session.refresh(task)
    return task

@router.get("/tasks")
def list_tasks(session: Session = Depends(get_session)):
    return session.exec(select(AgentTask).order_by(AgentTask.created_at.desc()).limit(50)).all()

@router.post("/tasks/{task_id}/approval")
def approve_task(task_id: int, data: ApprovalIn, session: Session = Depends(get_session)):
    task = session.get(AgentTask, task_id)
    if not task: raise HTTPException(404, "Task not found")
    task.status = "approved" if data.approved else "rejected"
    if data.note: task.summary = data.note
    session.add(task); session.commit(); session.refresh(task)
    return task
