import os
import socket
import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:1080/WebTours/index.htm"

@pytest.fixture(scope="session", autouse=True)
def ensure_server():
    """Démarre le serveur mock automatiquement sur GitHub Actions (dans le cloud GitHub)."""
    if os.getenv("GITHUB_ACTIONS"):
        from mock_server import start_server_in_thread
        server = start_server_in_thread()
        yield server
    else:
        yield None

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="function")
def browser(playwright_instance):
    # En environnement CI (GitHub Actions ou Jenkins), mode headless
    # En local, mode visible avec animation
    is_ci = bool(os.getenv("JENKINS_HOME") or os.getenv("CI") or os.getenv("GITHUB_ACTIONS"))
    browser = playwright_instance.chromium.launch(
        headless=True if is_ci else False,
        slow_mo=0 if is_ci else 300
    )
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
