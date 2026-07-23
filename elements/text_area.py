# elements/text_area.py
import allure
from tools.logger.logger import get_logger
from elements.base_element import BaseElement

logger = get_logger("TEXTAREA")

class Textarea(BaseElement):
    
    def get_locator(self, nth: int = 0, **kwargs):
        """Получить локатор textarea"""
        parent_locator = super().get_locator(nth, **kwargs)
        return parent_locator.locator('textarea').first
    
    def get_inner_text(self, nth: int = 0, **kwargs) -> str:
        """Получить текст из textarea"""
        locator = self.get_locator(nth, **kwargs)
        with allure.step(f"Getting visible text from {self.name} (nth: {nth})"):
            text = locator.inner_text()
            clean = text.strip()
            logger.info(f"Text of {self.name}: '{clean}'")
            return clean