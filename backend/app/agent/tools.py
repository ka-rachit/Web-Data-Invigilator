from langchain_core.tools import tool
from sqlmodel import Session
from ..db import engine
from ..vault import search_projects, profile_dict

@tool
def search_project_vault(query: str) -> list[dict]:
    """Search verified user project facts. Do not fabricate accomplishments, metrics, or technology claims."""
    with Session(engine) as session:
        return search_projects(session, query)

@tool
def get_saved_profile() -> dict:
    """Retrieve saved user profile fields for a form. Return only information the user saved."""
    with Session(engine) as session:
        return profile_dict(session)
