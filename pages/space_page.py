from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from elements.base_element import BaseElement
from elements.input import Input
from elements.text_area import Textarea
from tools.logger.logger import get_logger
logger = get_logger ("Login Page")

class SpacePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
       
        self.page_main_console_input = Input(page, '[data-test-id="command-input"]', 'Console Input') 
        self.page_main_console_status_red_label = BaseElement(page, '[data-test-id="status-red"]', 'Status Label Red')
        self.page_main_console_status_yellow_label = BaseElement(page, '[data-test-id="status-yellow"]', 'Status Label Yellow')
        self.page_main_console_status_green_label = BaseElement(page, '[data-test-id="status-green"]', 'Status Label Green')
        self.page_main_console_output = BaseElement(page, '[data-test-id="console-output"]', 'Console Reponse')     
                  
    def command_input(self, cmd: str):
        self.page_main_console_input.send_keys_character_by_character(cmd)
        self.page_main_console_input.check_have_value(cmd)
        self.page.keyboard.press('Enter')

    def get_reponse(self):
        self.page_main_console_output.get_inner_text()
        
        
