# elements/input.py
from playwright.sync_api import expect
from tools.logger.logger import get_logger
from elements.base_element import BaseElement

logger = get_logger("INPUT")

class Input(BaseElement):
    def get_locator(self, nth: int = 0, **kwargs):
        return super().get_locator(nth, **kwargs)
    
    def check_have_value(self, value: str, nth: int = 0, timeout: int = 30000, **kwargs):
        """Проверить, что поле ввода имеет определенное значение"""
        locator = self.get_locator(nth, **kwargs)
        expect(locator).to_have_value(value, timeout=timeout)
        logger.info(f"Verified {self.name} has value: '{value}' (nth: {nth})")
        return self
        
    def send_keys_character_by_character(self, value: str, nth: int = 0, timeout: int = 30000, **kwargs):
        """Ввести текст посимвольно"""
        locator = self.get_locator(nth, **kwargs)
        
        # Кликаем, очищаем, вводим
        locator.click(timeout=timeout)
        locator.clear(timeout=timeout)
        locator.press_sequentially(value, delay=0)
        
        # Проверяем
        actual_value = locator.input_value(timeout=timeout)
        assert actual_value == value, \
            f"Text entry failed for {self.name}. Expected: '{value}', Actual: '{actual_value}'"
        
        logger.info(f"Sent keys '{value}' to {self.name} (nth: {nth})")
        return self