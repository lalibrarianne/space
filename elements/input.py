from playwright.sync_api import expect, Locator
from tools.logger.logger import get_logger
from elements.base_element import BaseElement

logger = get_logger("INPUT")

class Input(BaseElement):
    def get_locator(self, nth: int = 0, **kwargs):
        return super().get_locator(nth, **kwargs)
    
    def fill(self, value: str, nth: int = 0, timeout: int | None = None, **kwargs):
        locator = self.get_locator(nth, **kwargs)
        locator.fill(value, timeout=timeout)
        expect(locator).to_have_value(value, timeout=timeout)
        logger.info(f"Filled {self.name} with: '{value}' (nth: {nth})")
            
    def check_have_value(self, value: str, nth: int = 0, timeout: int | None = None, **kwargs):
        locator = self.get_locator(nth, **kwargs)
        expect(locator).to_have_value(value, timeout=timeout)
        logger.info(f"Verified {self.name} has value: '{value}' (nth: {nth})")
            
    def clear_and_send_keys(self, value: str, nth: int = 0, timeout: int | None = None, **kwargs):
        locator = self.get_locator(nth, **kwargs)
        locator.clear(timeout=timeout)
        locator.fill(value, timeout=timeout)
        expect(locator).to_have_value(value, timeout=timeout)
        logger.info(f"Cleared and set value '{value}' for {self.name} (nth: {nth})")
            
    def clear(self, nth: int = 0, timeout: int | None = None, **kwargs):
        locator = self.get_locator(nth, **kwargs)
        locator.clear(timeout=timeout)
        logger.info(f"Cleared {self.name} (nth: {nth})")
            
    def send_keys(self, value: str, nth: int = 0, timeout: int | None = None, **kwargs):
        locator = self.get_locator(nth, **kwargs)
        locator.fill(value, timeout=timeout)
        expect(locator).to_have_value(value, timeout=timeout)
        logger.info(f"Sent keys '{value}' to {self.name} (nth: {nth})")
        
    def send_keys_character_by_character(self, value: str, nth: int = 0, timeout: int | None = None, max_attempts: int = 3, **kwargs):
        locator = self.get_locator(nth, **kwargs)
        
        for attempt in range(max_attempts):
            try:
                locator.click(timeout=timeout)
                self.page.wait_for_timeout(100)
                locator.clear(timeout=timeout)
                self.page.wait_for_timeout(100)
                # Select all and delete for additional clearing
                locator.press("Control+A")
                locator.press("Delete")
                self.page.wait_for_timeout(100)
                locator.press_sequentially(value, delay=0)
                actual_value = locator.input_value(timeout=timeout)             
                if actual_value == value:
                    logger.info(f"Sent keys '{value}' to {self.name} (nth: {nth})")
                    return
                else:
                    logger.warning(f"Attempt {attempt + 1}: Expected '{value}', but got '{actual_value}'")
                    if attempt < max_attempts - 1:
                        self.page.wait_for_timeout(100)
                        continue
                    else:
                        raise AssertionError(
                            f"Text entry failed for {self.name}. Expected: '{value}', Actual: '{actual_value}'"
                        )
                                           
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {self.name}: {str(e)}")
                if attempt < max_attempts - 1:
                    self.page.wait_for_timeout(100)
                    continue
                else:
                    raise AssertionError(
                        f"Failed to enter text '{value}' in {self.name} after {max_attempts} attempts. "
                        f"Last error: {str(e)}"
                    )
