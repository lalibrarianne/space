import os
import pytest
from typing import Generator
from _pytest.fixtures import SubRequest
from playwright.sync_api import Playwright, Page
from tools.playwright.pages import initialize_playwright_page
from io import StringIO


URL = os.getenv('TEST_URL')


HEADLESS = os.getenv('HEADLESS', 'true').lower() == 'true'
BROWSERS_CONFIG = StringIO(os.getenv('BROWSERS', 'chromium'))


@pytest.fixture(params=BROWSERS_CONFIG)
def page(request: SubRequest, playwright: Playwright) -> Generator[Page, None, None]:
    yield from initialize_playwright_page(
        playwright, 
        test_name=request.node.name,
        browser_type=request.param)


@pytest.fixture(scope="session")
def initialize_browser_state(playwright: Playwright):
    browser = playwright.chromium.launch(headless=HEADLESS)
    context = browser.new_context()
    page = context.new_page()
    browser.close()
