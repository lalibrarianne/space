# elements/base_element.py
from playwright.sync_api import Page, expect
import re
import allure
from tools.logger.logger import get_logger

logger = get_logger("BASE_ELEMENT")

class BaseElement:
    def __init__(self, page: Page, locator: str, name: str):
        self.page = page  
        self.name = name
        self.locator = locator
        
    def get_locator(self, nth: int = 0, **kwargs):
        """Получить локатор элемента"""
        formatted_locator = self.locator.format(**kwargs)
        locator = self.page.locator(formatted_locator).nth(nth)
        return locator
    
    def check_visible(self, nth: int = 0, timeout: int = 30000, **kwargs):
        """Проверить, что элемент видим"""
        locator = self.get_locator(nth, **kwargs)
        expect(locator).to_be_visible(timeout=timeout)
        logger.info(f"Element {self.name} is visible (nth: {nth})")
        return True