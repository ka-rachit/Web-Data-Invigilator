from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..db import get_session
from ..models import AgentTask
from ..security import require_n8n_token

router = APIRouter(prefix="/v1/n8n", tags=["n8n"], dependencies=[Depends(require_n8n_token)])

@router.post("/scan-start")
def scan_start(session: Session = Depends(get_session)):
    task = AgentTask(thread_id="monthly-personal-data-scan", task_type="personal_data_scan", status="pending_approval",
        summary="Monthly scan task queued; user approval required before browser activity.",
        payload={"scope": "user-approved public listings", "requires_user_approval": True})
    session.add(task); session.commit(); session.refresh(task)
    return {"task_id": task.id, "status": task.status, "message": task.summary}
