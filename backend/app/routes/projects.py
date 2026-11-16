from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session
from ..models import Project
from ..schemas import ProjectIn
from ..security import require_api_key

router = APIRouter(prefix="/v1/projects", tags=["projects"], dependencies=[Depends(require_api_key)])

@router.get("")
def list_projects(session: Session = Depends(get_session)):
    return session.exec(select(Project).order_by(Project.updated_at.desc())).all()

@router.post("")
def create_project(data: ProjectIn, session: Session = Depends(get_session)):
    project = Project(**data.model_dump())
    session.add(project); session.commit(); session.refresh(project)
    return project

@router.put("/{project_id}")
def update_project(project_id: int, data: ProjectIn, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project: raise HTTPException(404, "Project not found")
    for key, value in data.model_dump().items(): setattr(project, key, value)
    session.add(project); session.commit(); session.refresh(project)
    return project

@router.delete("/{project_id}")
def delete_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project: raise HTTPException(404, "Project not found")
    session.delete(project); session.commit()
    return {"deleted": True}
