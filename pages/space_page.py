from playwright.sync_api import Page
from pages.base_page import BasePage
from elements.base_element import BaseElement
from elements.input import Input
from tools.logger.logger import get_logger
import random
import allure

logger = get_logger("Space Page")

class SpacePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
       
        self.page_main_console_input = Input(page, '[data-test-id="command-input"]', 'Console Input') 
        self.page_main_console_status_red_label = BaseElement(page, '[data-test-id="status-red"]', 'Status Label Red')
        self.page_main_console_status_yellow_label = BaseElement(page, '[data-test-id="status-yellow"]', 'Status Label Yellow')
        self.page_main_console_status_green_label = BaseElement(page, '[data-test-id="status-green"]', 'Status Label Green')
        self.page_main_console_output = BaseElement(page, '[data-test-id="console-output"]', 'Console Response')     

    # ==================== МЕТОДЫ ДЛЯ ПРОВЕРКИ ОТВЕТА ====================
    
    def check_response_not_empty(self, response: str):
        """Проверить, что ответ не пустой"""
        assert response is not None, "Ответ от консоли равен None"
        assert len(response) > 0, "Ответ от консоли пустой"
        logger.info("Ответ успешно получен")
        return self
    
    def check_response_contains_keywords(self, response: str, keywords: list):
        """Проверить, что ответ содержит ключевые слова"""
        found_keywords = [kw for kw in keywords if kw in response.lower()]
        
        allure.attach(
            f"Найдены ключевые слова: {found_keywords}",
            name="keywords_check",
            attachment_type=allure.attachment_type.TEXT
        )
        
        assert len(found_keywords) > 0, \
            f"Ответ не содержит ожидаемых ключевых слов. Ожидалось: {keywords}"
        logger.info(f"Найдены ключевые слова: {found_keywords}")
        return self
    
    def check_command_help_output(self, response: str):
        """Проверить вывод команды help"""
        self.check_response_not_empty(response)
        self.check_response_contains_keywords(response, ["help", "clear", "date"])
        logger.info("Вывод команды help проверен успешно")
        return self

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ СО СТАТУСАМИ ====================
    
    def check_status_indicators_visible(self):
        """Проверить видимость всех статусных индикаторов"""
        self.page_main_console_status_red_label.check_visible()
        self.page_main_console_status_yellow_label.check_visible()
        self.page_main_console_status_green_label.check_visible()
        return self
    
    def check_status_red_visible(self):
        """Проверить видимость красного статуса"""
        self.page_main_console_status_red_label.check_visible()
        return self
    
    def check_status_yellow_visible(self):
        """Проверить видимость желтого статуса"""
        self.page_main_console_status_yellow_label.check_visible()
        return self
    
    def check_status_green_visible(self):
        """Проверить видимость зеленого статуса"""
        self.page_main_console_status_green_label.check_visible()
        return self

    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ С КОНСОЛЬЮ ====================

    def command_input(self, cmd: str):
        """Ввод команды в консоль"""
        self.page_main_console_input.send_keys_character_by_character(cmd)
        self.page_main_console_input.check_have_value(cmd)
        self.page.keyboard.press('Enter')
        logger.info(f"Команда '{cmd}' отправлена")
        return self

    def get_reponse(self) -> str:
        """Получить ответ от консоли"""
        locator = self.page_main_console_output.get_locator()
        lines = locator.locator('div').all()
        output_lines = []
        for line in lines:
            text = line.text_content()
            if text is not None and text.strip():
                output_lines.append(text.strip())
        response = '\n'.join(output_lines)
        logger.info(f"Получен ответ от консоли: {response[:100]}..." if response else "Ответ пустой")
        return response
    
    def get_last_response(self) -> str:
        """Получить последние строки ответа (после последней команды)"""
        full_output = self.get_reponse()
        if not full_output:
            return ""
        
        lines = full_output.split('\n')
        last_command_index = -1
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].startswith('>'):
                last_command_index = i
                break
        
        if last_command_index != -1:
            return '\n'.join(lines[last_command_index + 1:])
        return full_output
    
    def get_command_output(self, command: str) -> str:
        """Получить вывод конкретной команды"""
        self.command_input(command)
        response = self.get_reponse()
        if not response:
            return ""
        
        lines = response.split('\n')
        command_line = f'> {command}'
        
        command_index = -1
        for i, line in enumerate(lines):
            if line.strip() == command_line:
                command_index = i
                break
        
        if command_index != -1:
            output_lines = []
            for i in range(command_index + 1, len(lines)):
                if lines[i].startswith('>'):
                    break
                if lines[i].strip():
                    output_lines.append(lines[i])
            return '\n'.join(output_lines)
        
        return "Команда не найдена в выводе"
    
    def execute_and_get_output(self, command: str) -> str:
        """Выполнить команду и получить только ее вывод"""
        self.command_input(command)
        full_output = self.get_reponse()
        if not full_output:
            return ""
        
        lines = full_output.split('\n')
        command_line = f'> {command}'
        command_index = -1
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip() == command_line:
                command_index = i
                break
        
        if command_index == -1:
            return "Команда не найдена в выводе"
        
        output_lines = []
        for i in range(command_index + 1, len(lines)):
            if lines[i].startswith('>'):
                break
            if lines[i].strip():
                output_lines.append(lines[i])
        
        return '\n'.join(output_lines) if output_lines else "Вывод команды пустой"
    
    # ==================== МЕТОДЫ ДЛЯ РАБОТЫ СО СПИСКАМИ КОМАНД ====================

    def get_available_commands(self) -> list:
        """Получить список доступных команд"""
        return ["help", "clear", "date", "whoami", "neofetch"]
    
    def get_random_command(self) -> str:
        """Получить случайную команду из доступных"""
        commands = self.get_available_commands()
        return random.choice(commands)
    
    def execute_random_commands(self, count: int = 3) -> dict:
        """Выполнить несколько случайных команд и вернуть их вывод"""
        results = {}
        commands = self.get_available_commands()
        
        for i in range(count):
            cmd = random.choice(commands)
            output = self.execute_and_get_output(cmd)
            results[cmd] = output
        
        return results