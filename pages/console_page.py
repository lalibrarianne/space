# pages/console_page.py
from playwright.sync_api import Page, expect, Locator

class ConsolePage:
    def __init__(self, page: Page):
        self.page = page
        
        # Локаторы элементов (используем data-testid если есть, иначе CSS)
        self.console_input = page.locator('input[type="text"]').or_(
            page.locator('.console-input')
        ).or_(
            page.locator('#console-input')
        ).or_(
            page.locator('textarea')
        ).first
        
        self.console_output = page.locator('.console-output').or_(
            page.locator('#output')
        ).or_(
            page.locator('.terminal-output')
        ).or_(
            page.locator('.console-lines')
        ).first
        
        self.console_lines = page.locator('.console-line').or_(
            page.locator('.terminal-line')
        ).or_(
            page.locator('.output-line')
        )
        
        self.prompt_symbol = page.locator('.prompt').or_(
            page.locator('.console-prompt')
        ).or_(
            page.locator('[data-testid="prompt"]')
        ).first
        
        # Основной контейнер консоли
        self.console_container = page.locator('.console-container').or_(
            page.locator('.terminal')
        ).or_(
            page.locator('#console')
        ).first
    
    def load(self) -> 'ConsolePage':
        """Загрузка страницы и ожидание готовности консоли"""
        self.page.goto("https://exam.space-qa.site/")
        self.wait_for_console_ready()
        return self
    
    def wait_for_console_ready(self, timeout: int = 10000) -> None:
        """Ожидание загрузки консоли"""
        try:
            # Ожидаем появления поля ввода
            self.console_input.wait_for(state='visible', timeout=timeout)
            # Ожидаем появления вывода
            self.console_output.wait_for(state='visible', timeout=timeout)
            # Ожидаем появления приглашения
            self.prompt_symbol.wait_for(state='visible', timeout=timeout)
        except Exception as e:
            raise Exception(f"Консоль не загрузилась: {e}")
    
    def enter_command(self, command: str) -> 'ConsolePage':
        """Ввод команды в консоль"""
        # Ожидаем, что поле ввода готово
        self.console_input.wait_for(state='visible')
        
        # Очищаем и вводим команду
        self.console_input.clear()
        self.console_input.fill(command)
        
        # Нажимаем Enter для отправки
        self.console_input.press('Enter')
        
        # Ждем обработки команды
        self.wait_for_command_processed()
        return self
    
    def wait_for_command_processed(self, timeout: int = 5000) -> None:
        """Ожидание обработки команды (появление нового вывода)"""
        # Получаем текущее состояние вывода
        initial_lines_count = self.console_lines.count()
        
        # Ожидаем увеличения количества строк в выводе
        try:
            self.page.wait_for_function(
                f"""
                () => {{
                    const lines = document.querySelectorAll('.console-line, .terminal-line, .output-line');
                    return lines.length > {initial_lines_count};
                }}
                """,
                timeout=timeout
            )
        except Exception:
            # Если строки не увеличились, возможно вывод обновляется иначе
            # Ждем хотя бы появления нового текста
            initial_text = self.get_all_output()
            self.page.wait_for_function(
                f"""
                () => {{
                    const output = document.querySelector('.console-output, #output, .terminal-output, .console-lines');
                    return output && output.textContent !== '{initial_text}';
                }}
                """,
                timeout=timeout
            )
    
    def get_last_output(self) -> str:
        """Получение последней строки вывода"""
        lines = self.console_lines.all()
        if lines:
            return lines[-1].text_content().strip()
        return ""
    
    def get_all_output(self) -> str:
        """Получение всего текста вывода"""
        return self.console_output.text_content().strip()
    
    def get_prompt_text(self) -> str:
        """Получение текста приглашения консоли"""
        return self.prompt_symbol.text_content().strip()
    
    def is_console_visible(self) -> bool:
        """Проверка видимости консоли"""
        try:
            return self.console_container.is_visible() and self.console_input.is_visible()
        except:
            return False
    
    def get_output_lines(self) -> list:
        """Получение списка всех строк вывода"""
        return [line.text_content().strip() for line in self.console_lines.all()]
    
    def wait_for_output_contains(self, text: str, timeout: int = 5000) -> bool:
        """Ожидание появления текста в выводе"""
        try:
            self.console_output.wait_for(timeout=timeout)
            self.page.wait_for_function(
                f"""
                () => {{
                    const output = document.querySelector('.console-output, #output, .terminal-output, .console-lines');
                    return output && output.textContent.includes('{text}');
                }}
                """,
                timeout=timeout
            )
            return True
        except Exception:
            return False
    
    def clear_console(self) -> 'ConsolePage':
        """Очистка консоли (если поддерживается)"""
        self.enter_command("clear")
        return self
    
    def get_command_history(self) -> list:
        """Получение истории команд (если доступна)"""
        # Зависит от реализации приложения
        history = self.page.locator('.command-history').or_(
            self.page.locator('[data-testid="history"]')
        )
        if history.count() > 0:
            return [item.text_content().strip() for item in history.all()]
        return []