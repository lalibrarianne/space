from __future__ import annotations

from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        
    def visit(self, url: str):
        self.link.goto(url)
        return self
