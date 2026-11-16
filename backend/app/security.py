import secrets
from fastapi import Header, HTTPException
from .config import settings

def require_api_key(authorization: str | None = Header(default=None)):
    if not authorization or not secrets.compare_digest(authorization, f"Bearer {settings.app_api_key}"):
        raise HTTPException(status_code=401, detail="Missing or invalid bearer API key")

def require_n8n_token(x_n8n_token: str | None = Header(default=None)):
    if not x_n8n_token or not secrets.compare_digest(x_n8n_token, settings.n8n_webhook_token):
        raise HTTPException(status_code=401, detail="Missing or invalid n8n webhook token")
