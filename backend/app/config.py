from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    app_api_key: str = "dev-local-key-change-me"
    n8n_webhook_token: str = "change-this-n8n-token"
    database_url: str = "sqlite:///./data/webagent.db"
    enable_browser: bool = True
    headless: bool = False
    browser_profile_dir: str = "./data/browser-profile"

    @property
    def profile_path(self) -> Path:
        path = Path(self.browser_profile_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

settings = Settings()
