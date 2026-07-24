# tests/test.py - с обработкой исключений
import pytest
import allure
import re
import random
from pages.space_page import SpacePage

@allure.epic("Space Console")
@allure.feature("Console Status Indicators")
class TestSpaceConsoleStatus:
    
    @allure.story("Status Labels Visibility")
    @allure.title("Проверка видимости статусных индикаторов на странице")
    def test_status_labels_visibility(self, space_page: SpacePage):
        try:
            with allure.step("Проверить видимость всех статусных индикаторов"):
                space_page.check_status_indicators_visible()
        except Exception as e:
            allure.attach(
                str(e),
                name="test_failure_details",
                attachment_type=allure.attachment_type.TEXT
            )
            raise


@allure.epic("Space Console")
@allure.feature("Console Commands")
class TestSpaceConsoleCommands:
    
    @allure.story("Help Command")
    @allure.title("Ввод команды help и проверка ответа")
    def test_help_command(self, space_page: SpacePage):
        try:
            with allure.step("Ввести команду 'help' в консоль"):
                space_page.command_input("help")

            with allure.step("Получить ответ от консоли"):
                response = space_page.get_reponse()
                
                allure.attach(
                    str(response) if response else "Ответ пустой (None)",
                    name="console_response",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                help_output = space_page.get_command_output("help")
                allure.attach(
                    str(help_output) if help_output else "Вывод команды help пустой",
                    name="help_command_output",
                    attachment_type=allure.attachment_type.TEXT
                )

            with allure.step("Проверить, что ответ содержит информацию о командах"):
                space_page.check_command_help_output(response)
        except Exception as e:
            allure.attach(
                str(e),
                name="test_failure_details",
                attachment_type=allure.attachment_type.TEXT
            )
            raise

    @allure.story("Unknown Command")
    @allure.title("Проверка обработки неизвестной команды")
    def test_unknown_command(self, space_page: SpacePage):
        try:
            unknown_cmd = "test_unknown_command_123"
            
            with allure.step(f"Ввести неизвестную команду '{unknown_cmd}'"):
                output = space_page.get_command_output(unknown_cmd)
                
                allure.attach(
                    str(output) if output else "Вывод пустой",
                    name="unknown_command_output",
                    attachment_type=allure.attachment_type.TEXT
                )

            with allure.step("Проверить, что консоль сообщает об ошибке"):
                assert output is not None, "Нет вывода для неизвестной команды"
                assert "Unknown command" in output or "not found" in output.lower(), \
                    f"Неизвестная команда не обработана должным образом. Вывод: {output}"
        except Exception as e:
            allure.attach(
                str(e),
                name="test_failure_details",
                attachment_type=allure.attachment_type.TEXT
            )
            raise

    @allure.story("Console Response")
    @allure.title("Проверка получения вывода конкретной команды")
    def test_get_command_output(self, space_page: SpacePage):
        try:
            with allure.step("Получить вывод команды 'whoami'"):
                output = space_page.execute_and_get_output("whoami")
                
                allure.attach(
                    str(output) if output else "Вывод пустой",
                    name="whoami_output",
                    attachment_type=allure.attachment_type.TEXT
                )

            with allure.step("Проверить, что вывод содержит ожидаемый текст"):
                assert output is not None, "Вывод команды whoami пустой"
                assert "Natali" in output or "Greetings" in output, \
                    f"Вывод команды whoami не содержит ожидаемого текста: {output}"
        except Exception as e:
            allure.attach(
                str(e),
                name="test_failure_details",
                attachment_type=allure.attachment_type.TEXT
            )
            raise

@allure.epic("Space Console")
@allure.feature("Combined Tests")
class TestSpaceConsoleCombined:

    @allure.story("Random Commands")
    @allure.title("Выполнение случайных команд")
    def test_random_commands_execution(self, space_page: SpacePage):
        try:
            with allure.step("Получить список доступных команд"):
                available_commands = space_page.get_available_commands()
                allure.attach(
                    f"Доступные команды: {available_commands}",
                    name="available_commands",
                    attachment_type=allure.attachment_type.TEXT
                )
            
            with allure.step("Выполнить 5 случайных команд"):
                results = space_page.execute_random_commands(count=5)
                
                summary = "Результаты выполнения случайных команд:\n\n"
                for cmd, output in results.items():
                    status = "✅ Успешно" if output and len(output) > 0 else "❌ Ошибка"
                    summary += f"{cmd}: {status}\n"
                    if output and len(output) > 0:
                        summary += f"  Вывод: {output[:100]}...\n\n"
                
                allure.attach(
                    summary,
                    name="random_commands_summary",
                    attachment_type=allure.attachment_type.TEXT
                )
            
            with allure.step("Проверить, что все команды выполнены"):
                for cmd, output in results.items():
                    assert output is not None, f"Команда '{cmd}' не выполнена"
                    if cmd != "clear":
                        assert len(output) > 0, f"Команда '{cmd}' вернула пустой вывод"
        except Exception as e:
            allure.attach(
                str(e),
                name="test_failure_details",
                attachment_type=allure.attachment_type.TEXT
            )
            raise

    @allure.story("All Commands")
    @allure.title("Выполнение всех доступных команд")
    def test_all_commands_execution(self, space_page: SpacePage):
        try:
            all_commands = ["help", "whoami", "date", "neofetch"]
            results = {}
            
            with allure.step("Выполнить все команды"):
                for cmd in all_commands:
                    with allure.step(f"Выполнить команду '{cmd}'"):
                        output = space_page.execute_and_get_output(cmd)
                        results[cmd] = output
                        
                        allure.attach(
                            str(output) if output else f"Вывод команды '{cmd}' пустой",
                            name=f"command_{cmd}_output",
                            attachment_type=allure.attachment_type.TEXT
                        )
            
            with allure.step("Проверить вывод каждой команды"):
                assert "help" in results["help"].lower(), "help не найден в выводе help"
                assert "clear" in results["help"].lower(), "clear не найден в выводе help"
                assert "date" in results["help"].lower(), "date не найден в выводе help"
                
                assert "Natali" in results["whoami"] or "Greetings" in results["whoami"], \
                    "whoami не вернул ожидаемое приветствие"
                
                assert re.search(r'\d{4}/\d{2}/\d{2}', results["date"]), \
                    "date не вернул дату в ожидаемом формате"
                
                assert "OS" in results["neofetch"], "neofetch не содержит OS"
                assert "CPU" in results["neofetch"], "neofetch не содержит CPU"
                assert "Memory" in results["neofetch"], "neofetch не содержит Memory"
                
            with allure.step("Проверить, что все команды выполнены успешно"):
                for cmd, output in results.items():
                    assert output is not None, f"Команда '{cmd}' не выполнена"
                    assert len(output) > 0, f"Команда '{cmd}' вернула пустой вывод"
        except Exception as e:
            allure.attach(
                str(e),
                name="test_failure_details",
                attachment_type=allure.attachment_type.TEXT
            )
            raise