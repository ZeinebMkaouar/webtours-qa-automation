import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:1080/WebTours/index.htm"

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="function")
def browser(playwright_instance):
    # Mode headless activé par défaut (idéal pour Jenkins et exécution rapide)
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(1000)
    yield page
    context.close()
