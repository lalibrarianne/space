from playwright.sync_api import Page, expect
import re
import allure
from tools.logger.logger import get_logger
import time
from typing import List

logger = get_logger("BASE_ELEMENT")

class BaseElement:
    def __init__(self, page: Page, locator: str, name: str):
        self.page = page  
        self.name = name
        self.locator = locator
        
    def get_locator(self, nth: int = 0, timeout: int | None = None, **kwargs):
        formatted_locator = self.locator.format(**kwargs)
        locator = self.page.locator(formatted_locator).nth(nth)
        return locator
    
    def click(self, nth: int = 0, timeout: int | None = None, force: bool = False, **kwargs):
        locator = self.get_locator(nth, **kwargs)
        if force:
            locator.evaluate('element => element.click()')
        else:
            locator.click(timeout=50000)
        logger.info(f"Clicked on {self.name} (nth: {nth})")

    def check_not_visible(self, nth: int = 0, timeout: int | None = None, **kwargs):
        locator = self.get_locator(nth, **kwargs)
        expect(locator).not_to_be_visible(timeout=timeout)
        logger.info(f"Element {self.name} is not visible (nth: {nth})")                     
            
    def check_visible(self, nth: int = 0, timeout: int | None = None, **kwargs):
        locator = self.get_locator(nth, **kwargs)
        expect(locator).to_be_visible(timeout=timeout or 30000)
        logger.info(f"Element {self.name} is visible (nth: {nth})")  

    def check_have_text(self, text: str, nth: int = 0, timeout: int | None = None, **kwargs):
        locator = self.get_locator(nth, **kwargs)
        expect(locator).to_contain_text(re.compile(text, re.IGNORECASE), timeout=timeout)
        logger.info(f"Element {self.name} has text {text}") 
        
    def get_inner_text(self, nth: int = 0, **kwargs) -> str:
        """
        Fetches the visible text content of this element, mirrors what a user sees.
        """
        locator = self.get_locator(nth, **kwargs)
        with allure.step(f"Getting visible text from {self.name} (nth: {nth})"):
            text = locator.inner_text()
            clean = text.strip()
            logger.info(f"Text of {self.name}: '{clean}'")
            return clean
 