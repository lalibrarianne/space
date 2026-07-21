import allure
from tools.logger.logger import get_logger
from elements.base_element import BaseElement
from typing import List

logger = get_logger("TEXTAREA")

class Textarea(BaseElement):
    
    def get_locator(self, nth: int = 0, **kwargs):
        parent_locator = super().get_locator(nth, **kwargs)
        return parent_locator.locator('textarea').first
    
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

    def get_input_value_text(self, nth: int = 0, **kwargs) -> str:
        """
        Reads the *value* of an input-like element, exactly as set in the DOM.
        """
        locator = self.get_locator(nth, **kwargs)
        with allure.step(f"Getting input value from {self.name} (nth: {nth})"):
            text = locator.input_value()
            logger.info(f"Got input-value from {self.name} (length: {len(text)} chars) (nth: {nth})")
            return text
        
    def all_text_contents(self, nth: int = 0, expand_dropdown: bool = True, **kwargs) -> List [str]:
        locator = self.get_locator(nth, **kwargs)
        with allure.step(f"Getting all elements from {self.name} (nth: {nth})"):
            if expand_dropdown:
                try:
                    locator.click(timeout=5000)
                    logger.info(f"Expanded dropdown {self.name}")
                except Exception as e:
                    logger.warning(f"Could not click dropdown {self.name}: {e}")
            try:
                text_list = locator.all_text_contents()
                cleaned_list = []
                for text in text_list:
                    if text and text.strip():
                        cleaned_list.append(text.strip())
                logger.info(f"Elements {self.name}: {cleaned_list}")
                return cleaned_list
        
            except Exception as e:
                logger.error (f"Failed to get text contents from {self.name}: {e}")
                return []
            
    