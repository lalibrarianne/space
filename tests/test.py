# tests/test_space_page.py
import pytest
import allure
from pages.space_page import SpacePage
from tools.logger.logger import get_logger
from fixtures.browsers import page


@allure.epic("Space Console")
@allure.feature("Console Status Indicators")
class TestSpaceConsoleStatus:
    
    @allure.story("Status Labels Visibility")
    @allure.title("Проверка видимости статусных индикаторов на странице")
    @allure.description("Тест проверяет, что все три статусных индикатора (красный, желтый, зеленый) отображаются на странице")
    def test_status_labels_visibility(self, space_page: SpacePage, page):
        with allure.step("Открыть страницу консоли"):
            page.goto("https://exam.space-qa.site/")
            page.wait_for_load_state("networkidle")
        
        with allure.step("Проверить видимость красного статусного индикатора"):
            space_page.page_main_console_status_red_label.check_visible()
        
        with allure.step("Проверить видимость желтого статусного индикатора"):
            space_page.page_main_console_status_yellow_label.check_visible()
        
        with allure.step("Проверить видимость зеленого статусного индикатора"):
            space_page.page_main_console_status_green_label.check_visible()
        
        with allure.step("Проверить, что консольный ввод также видим"):
            space_page.page_main_console_input.check_visible()
        
        with allure.step("Проверить, что консольный вывод также видим"):
            space_page.page_main_console_output.check_visible()

    @allure.story("Status Labels Combined")
    @allure.title("Комплексная проверка всех статусных индикаторов")
    @allure.description("Тест проверяет видимость и текст всех статусных индикаторов одновременно")
    def test_all_status_labels(self, space_page: SpacePage, page):
        with allure.step("Открыть страницу консоли"):
            page.goto("https://exam.space-qa.site/")
            page.wait_for_load_state("networkidle")
        
        status_labels = [
            (space_page.page_main_console_status_red_label, "Red", "красный"),
            (space_page.page_main_console_status_yellow_label, "Yellow", "желтый"),
            (space_page.page_main_console_status_green_label, "Green", "зеленый")
        ]
        
        for label, expected_text, color_name in status_labels:
            with allure.step(f"Проверить {color_name} статусный индикатор"):
                label.check_visible(timeout=5000)
                label.check_have_text(expected_text, timeout=5000)
                allure.attach(
                    f"Статус '{expected_text}' отображается корректно",
                    name=f"{color_name}_status_check",
                    attachment_type=allure.attachment_type.TEXT
                )


@allure.epic("Space Console")
@allure.feature("Console Commands")
class TestSpaceConsoleCommands:
    
    @allure.story("Help Command")
    @allure.title("Ввод команды help и проверка ответа")
    @allure.description("Тест проверяет, что команда 'help' выполняется и возвращает ожидаемый ответ")
    def test_help_command(self, space_page: SpacePage, page):
        with allure.step("Открыть страницу консоли"):
            page.goto("https://exam.space-qa.site/")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1000)  # Небольшая пауза для загрузки консоли
        
        with allure.step("Ввести команду 'help' в консоль"):
            space_page.command_input("help")
            page.wait_for_timeout(2000)  # Ожидание обработки команды
        
        with allure.step("Получить ответ от консоли"):
            response = space_page.get_reponse()
            allure.attach(
                str(response),
                name="console_response",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("Проверить, что ответ содержит информацию о командах"):
            assert response is not None, "Ответ от консоли пустой"
            assert len(response) > 0, "Ответ от консоли пустой"
            
            # Проверяем наличие ключевых слов в ответе
            expected_keywords = ["help", "available", "commands"]
            found_keywords = [keyword for keyword in expected_keywords if keyword.lower() in response.lower()]
            
            allure.attach(
                f"Найдены ключевые слова: {found_keywords}",
                name="keywords_found",
                attachment_type=allure.attachment_type.TEXT
            )
            
            assert len(found_keywords) > 0, \
                f"Ответ не содержит ожидаемых ключевых слов. Ожидалось: {expected_keywords}. Получено: {response[:200]}..."
            
            logger.info(f"Команда help выполнена успешно. Ответ: {response[:100]}...")

    @allure.story("Help Command")
    @allure.title("Ввод команды help и проверка наличия списка команд")
    @allure.description("Тест проверяет, что команда 'help' возвращает список доступных команд")
    def test_help_command_returns_commands_list(self, space_page: SpacePage, page):
        with allure.step("Открыть страницу консоли"):
            page.goto("https://exam.space-qa.site/")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1000)
        
        with allure.step("Ввести команду 'help' и получить ответ"):
            space_page.command_input("help")
            page.wait_for_timeout(2000)
            response = space_page.get_reponse()
        
        with allure.step("Проверить, что ответ содержит несколько строк (список команд)"):
            # Разбиваем ответ на строки
            lines = response.split('\n') if response else []
            allure.attach(
                f"Количество строк в ответе: {len(lines)}",
                name="response_lines_count",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # В ответе должно быть больше одной строки (приветствие + список команд)
            assert len(lines) > 1, f"Ответ содержит только {len(lines)} строк. Ожидается больше."
        
        with allure.step("Проверить, что в ответе есть хотя бы одна команда"):
            # Ищем команды в ответе (обычно они перечислены через запятую или в столбик)
            command_indicators = ["help", "clear", "exit", "list", "show", "status"]
            found_commands = [cmd for cmd in command_indicators if cmd in response.lower()]
            
            allure.attach(
                f"Найдены команды: {found_commands}",
                name="found_commands",
                attachment_type=allure.attachment_type.TEXT
            )
            
            assert len(found_commands) > 0, \
                f"В ответе не найдено ни одной известной команды. Проверьте формат вывода."

    @allure.story("Help Command")
    @allure.title("Повторный ввод команды help")
    @allure.description("Тест проверяет стабильность консоли при повторном вводе команды help")
    def test_help_command_multiple_times(self, space_page: SpacePage, page):
        with allure.step("Открыть страницу консоли"):
            page.goto("https://exam.space-qa.site/")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1000)
        
        responses = []
        
        for i in range(3):
            with allure.step(f"Ввести команду 'help' (попытка {i+1})"):
                space_page.command_input("help")
                page.wait_for_timeout(1500)
                response = space_page.get_reponse()
                responses.append(response)
                
                allure.attach(
                    f"Ответ {i+1}: {response[:100]}...",
                    name=f"response_{i+1}",
                    attachment_type=allure.attachment_type.TEXT
                )
        
        with allure.step("Проверить, что все ответы не пустые"):
            for i, response in enumerate(responses):
                assert response is not None, f"Ответ {i+1} пустой"
                assert len(response) > 0, f"Ответ {i+1} пустой"
        
        with allure.step("Проверить, что консоль стабильна после всех команд"):
            # Проверяем видимость ввода после команд
            space_page.page_main_console_input.check_visible(timeout=5000)
            space_page.page_main_console_output.check_visible(timeout=5000)
            
            # Проверяем, что статусные индикаторы все еще видны
            space_page.page_main_console_status_red_label.check_visible(timeout=3000)
            space_page.page_main_console_status_yellow_label.check_visible(timeout=3000)
            space_page.page_main_console_status_green_label.check_visible(timeout=3000)


@allure.epic("Space Console")
@allure.feature("Console Input/Output")
class TestSpaceConsoleIO:
    
    @allure.story("Console Input")
    @allure.title("Проверка ввода текста в консоль")
    @allure.description("Тест проверяет, что текст корректно вводится в консольное поле")
    def test_console_input_text(self, space_page: SpacePage, page):
        test_command = "test_input"
        
        with allure.step("Открыть страницу консоли"):
            page.goto("https://exam.space-qa.site/")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1000)
        
        with allure.step(f"Ввести текст '{test_command}' в консоль"):
            space_page.page_main_console_input.send_keys_character_by_character(test_command)
        
        with allure.step("Проверить, что текст введен корректно"):
            space_page.page_main_console_input.check_have_value(test_command)
        
        with allure.step("Проверить, что консольный ввод видим"):
            space_page.page_main_console_input.check_visible()

    @allure.story("Console Response")
    @allure.title("Проверка получения ответа от консоли")
    @allure.description("Тест проверяет, что метод get_reponse() возвращает текст")
    def test_console_get_response(self, space_page: SpacePage, page):
        with allure.step("Открыть страницу консоли"):
            page.goto("https://exam.space-qa.site/")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1000)
        
        with allure.step("Ввести команду 'help'"):
            space_page.command_input("help")
            page.wait_for_timeout(2000)
        
        with allure.step("Получить ответ от консоли"):
            response = space_page.get_reponse()
            
            allure.attach(
                f"Получен ответ длиной {len(response) if response else 0} символов",
                name="response_info",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("Проверить, что ответ получен"):
            assert response is not None, "Метод get_reponse() вернул None"
            assert isinstance(response, str), "Метод get_reponse() должен возвращать строку"


@allure.epic("Space Console")
@allure.feature("Combined Tests")
class TestSpaceConsoleCombined:
    
    @allure.story("Full Flow")
    @allure.title("Полный сценарий: статусы + команда help")
    @allure.description("Комплексный тест, проверяющий статусы и выполнение команды help")
    def test_full_flow_status_and_help(self, space_page: SpacePage, page):
        with allure.step("Открыть страницу консоли"):
            page.goto("https://exam.space-qa.site/")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1000)
        
        with allure.step("Проверить все статусные индикаторы"):
            # Проверяем видимость всех статусов
            statuses = [
                ("красный", space_page.page_main_console_status_red_label),
                ("желтый", space_page.page_main_console_status_yellow_label),
                ("зеленый", space_page.page_main_console_status_green_label)
            ]
            
            for color_name, label in statuses:
                with allure.step(f"Проверить {color_name} статус"):
                    label.check_visible(timeout=5000)
            
            # Проверяем, что все статусы видны одновременно
            red_visible = space_page.page_main_console_status_red_label.check_visible(timeout=3000)
            yellow_visible = space_page.page_main_console_status_yellow_label.check_visible(timeout=3000)
            green_visible = space_page.page_main_console_status_green_label.check_visible(timeout=3000)
        
        with allure.step("Ввести команду 'help' и получить ответ"):
            space_page.command_input("help")
            page.wait_for_timeout(2000)
            response = space_page.get_reponse()
            
            allure.attach(
                response,
                name="help_command_response",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("Проверить, что ответ содержит информацию о командах"):
            assert response is not None, "Ответ от консоли пустой"
            assert "help" in response.lower() or "available" in response.lower(), \
                f"Ответ не содержит информации о командах: {response[:100]}..."
        
        with allure.step("Проверить, что статусные индикаторы все еще видны после команды"):
            space_page.page_main_console_status_red_label.check_visible(timeout=3000)
            space_page.page_main_console_status_yellow_label.check_visible(timeout=3000)
            space_page.page_main_console_status_green_label.check_visible(timeout=3000)
        
        with allure.step("Проверить, что поле ввода все еще активно"):
            space_page.page_main_console_input.check_visible(timeout=3000)
            space_page.page_main_console_input.check_have_value("")