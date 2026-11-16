from sqlmodel import Session, select
from .models import Project, UserProfile

def search_projects(session: Session, query: str) -> list[dict]:
    q = query.strip().lower()
    rows = session.exec(select(Project)).all()
    terms = q.split()
    result = []
    for p in rows:
        corpus = " ".join([p.name, p.description, *p.technologies, str(p.facts)]).lower()
        if not q or any(term in corpus for term in terms):
            result.append({"id": p.id, "name": p.name, "description": p.description, "technologies": p.technologies, "facts": p.facts})
    return result[:10]

def profile_dict(session: Session) -> dict:
    p = session.get(UserProfile, 1)
    if not p:
        return {}
    return {"full_name": p.full_name, "email": p.email, "phone": p.phone, "education": p.education, "location": p.location, "additional_details": p.additional_details}
