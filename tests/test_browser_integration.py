import os, pytest
@pytest.mark.integration
@pytest.mark.asyncio
async def test_local_stagehand_example_domain():
    if os.getenv("RUN_BROWSER_INTEGRATION") != "1": pytest.skip("Set RUN_BROWSER_INTEGRATION=1 to run real browser + Gemini integration")
    from backend.app.agent.browser import create_stagehand
    browser, stagehand = await create_stagehand()
    try:
        page = await browser.context.active_page()
        await page.goto("https://example.com")
        assert "Example Domain" in await page.title()
        extracted = await stagehand.extract("Extract the main page heading")
        assert extracted is not None
    finally:
        await stagehand.close(); await browser.close()
