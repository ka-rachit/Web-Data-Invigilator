from pydantic import BaseModel, Field
from typing import Any

class ProfileIn(BaseModel):
    full_name: str = ""
    email: str = ""
    phone: str = ""
    education: str = ""
    location: str = ""
    additional_details: dict[str, Any] = Field(default_factory=dict)

class ProjectIn(BaseModel):
    name: str
    description: str
    technologies: list[str] = Field(default_factory=list)
    facts: dict[str, Any] = Field(default_factory=dict)

class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    thread_id: str = Field(default="default", min_length=1, max_length=128)

class FormAssistIn(BaseModel):
    page_url: str = Field(max_length=2048)
    page_title: str = Field(default="", max_length=512)
    fields: list[dict[str, Any]] = Field(max_length=100)
    user_instruction: str = Field(default="Suggest values based on saved profile and project vault; do not submit.", max_length=4000)

class ApprovalIn(BaseModel):
    approved: bool
    note: str = ""
