from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON, Text

def utcnow():
    return datetime.now(timezone.utc)

class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=1, primary_key=True)
    full_name: str = ""
    email: str = ""
    phone: str = ""
    education: str = ""
    location: str = ""
    additional_details: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    updated_at: datetime = Field(default_factory=utcnow)

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str = Field(sa_column=Column(Text, nullable=False))
    technologies: list[str] = Field(default_factory=list, sa_column=Column(JSON, nullable=False))
    facts: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)

class AgentTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    thread_id: str = Field(index=True)
    task_type: str = "agent"
    status: str = "pending_approval"
    summary: str = ""
    payload: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)

class ApplicationRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str
    role: str
    url: str = ""
    status: str = "draft"
    notes: str = ""
    created_at: datetime = Field(default_factory=utcnow)
