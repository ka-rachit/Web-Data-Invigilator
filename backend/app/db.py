from pathlib import Path
from sqlmodel import SQLModel, Session, create_engine
from .config import settings

if settings.database_url.startswith("sqlite:///"):
    raw = settings.database_url.replace("sqlite:///", "", 1)
    if raw and raw != ":memory:":
        Path(raw).parent.mkdir(parents=True, exist_ok=True)
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args, pool_pre_ping=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
