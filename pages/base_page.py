from __future__ import annotations

import allure
from playwright.sync_api import Page
from typing import Dict, Pattern, Optional, TYPE_CHECKING
from elements.base_element import BaseElement
from tools.logger.logger import get_logger



class BasePage:
    def __init__(self, page: Page):
        self.page = page
        
        
    def visit(self, url: str):
        self.link.goto(url)

    @allure.step("Reload page")
    def reload(self):
        with allure.step("Reloading current page"):
            self.link.reload()

    @allure.step("Check current URL")
    def check_current_url(self, expected_url: Pattern[str]):
        with allure.step(f"Verifying URL matches pattern: {expected_url.pattern}"):
            self.link.check_current_url(expected_url)

    