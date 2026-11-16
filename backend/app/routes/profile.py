from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..db import get_session
from ..models import UserProfile
from ..schemas import ProfileIn
from ..security import require_api_key

router = APIRouter(prefix="/v1/profile", tags=["profile"], dependencies=[Depends(require_api_key)])

@router.get("")
def read_profile(session: Session = Depends(get_session)):
    return session.get(UserProfile, 1) or {"id": 1, "full_name": "", "email": "", "phone": "", "education": "", "location": "", "additional_details": {}}

@router.put("")
def save_profile(data: ProfileIn, session: Session = Depends(get_session)):
    profile = session.get(UserProfile, 1) or UserProfile(id=1)
    for key, value in data.model_dump().items():
        setattr(profile, key, value)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile
