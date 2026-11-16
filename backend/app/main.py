from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .db import create_db_and_tables
from .security import require_api_key
from .routes import profile, projects, agent, n8n

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    app.state.agent = None; app.state.browser = None; app.state.stagehand = None
    if settings.enable_browser and settings.gemini_api_key:
        try:
            from .agent.browser import create_stagehand
            from .agent.factory import create_agent
            browser, stagehand = await create_stagehand()
            app.state.browser, app.state.stagehand = browser, stagehand
            app.state.agent = create_agent(stagehand)
        except Exception as exc:
            app.state.startup_error = str(exc)
    yield
    if app.state.stagehand:
        try: await app.state.stagehand.close()
        except Exception: pass
    if app.state.browser:
        try: await app.state.browser.close()
        except Exception: pass

app = FastAPI(title="Personal Web Agent", version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False,
                   allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                   allow_headers=["Authorization", "Content-Type", "X-N8N-Token"])
app.include_router(profile.router); app.include_router(projects.router); app.include_router(agent.router); app.include_router(n8n.router)

@app.get("/health")
def health():
    return {"status": "ok", "agent_ready": app.state.agent is not None, "startup_error": getattr(app.state, "startup_error", None)}

@app.get("/v1/status", dependencies=[Depends(require_api_key)])
def status():
    return {"agent_ready": app.state.agent is not None, "model": settings.gemini_model}
