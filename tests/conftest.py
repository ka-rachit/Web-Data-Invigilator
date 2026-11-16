import os
os.environ["DATABASE_URL"] = "sqlite:///./data/test_webagent.db"
os.environ["ENABLE_BROWSER"] = "false"
os.environ["GEMINI_API_KEY"] = ""
os.environ["APP_API_KEY"] = "test-key"
os.environ["N8N_WEBHOOK_TOKEN"] = "test-n8n-token"
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.db import create_db_and_tables

@pytest.fixture
def client():
    create_db_and_tables()
    with TestClient(app) as c: yield c

@pytest.fixture
def auth_headers(): return {"Authorization": "Bearer test-key"}
