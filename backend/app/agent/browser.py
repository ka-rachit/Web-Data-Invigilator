from stagehand import Stagehand, local_browser
from ..config import settings

async def create_stagehand():
    browser = await local_browser.launch(
        headless=settings.headless,
        user_data_dir=str(settings.profile_path),
        preserve_user_data_dir=True,
    )
    stagehand = await Stagehand.create(
        browser=browser,
        model=f"google/{settings.gemini_model}",
        model_api_key=settings.gemini_api_key,
    )
    return browser, stagehand
