# tools/playwright/pages.py
import os
import allure
from typing import Generator
from playwright.sync_api import Playwright, Page
from dotenv import load_dotenv

load_dotenv()

# Browser configuration
SLOW_MO = int(os.getenv('SLOW_MO', '0'))
HEADLESS = os.getenv('HEADLESS', 'true').lower() == 'true'
RECORD_VIDEO = os.getenv('RECORD_VIDEO', 'false').lower() == 'true'
RECORD_TRACING = os.getenv('RECORD_TRACING', 'false').lower() == 'true'
browser_channel = os.getenv('BROWSER_CHANNEL')

# Timeout configurations (in milliseconds)
NAVIGATION_TIMEOUT = int(os.getenv('NAVIGATION_TIMEOUT', '30000'))
ACTION_TIMEOUT = int(os.getenv('ACTION_TIMEOUT', '20000'))
BROWSER_LAUNCH_TIMEOUT = int(os.getenv('BROWSER_LAUNCH_TIMEOUT', '30000'))


def initialize_playwright_page(
        playwright: Playwright,
        test_name: str,
        browser_type: str) -> Generator[Page, None, None]:
    """Инициализация страницы Playwright для тестов"""
    
    # Создаем папки для записей, если включены
    if RECORD_VIDEO:
        os.makedirs('./videos', exist_ok=True)
    if RECORD_TRACING:
        os.makedirs('./tracing', exist_ok=True)
    
    # Настройки контекста
    context_options = {
        'viewport': {'width': 1280, 'height': 720},
    }
    
    # Добавляем видео, если включено
    if RECORD_VIDEO:
        context_options['record_video_dir'] = './videos'
        context_options['record_video_size'] = {"width": 1280, "height": 720}
    
    # Настройки запуска браузера
    launch_args = {
        'headless': HEADLESS,
        'timeout': BROWSER_LAUNCH_TIMEOUT,
        'slow_mo': SLOW_MO,
        'args': []
    }
    
    if browser_channel:
        launch_args['channel'] = browser_channel
    
    # Запускаем браузер и создаем контекст
    browser = playwright[browser_type].launch(**launch_args)
    context = browser.new_context(**context_options)
    
    # Устанавливаем таймауты
    context.set_default_timeout(ACTION_TIMEOUT)
    context.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
    
    # Запускаем трейсинг, если включен
    if RECORD_TRACING:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    # Создаем страницу
    page = context.new_page()
    page.set_default_timeout(ACTION_TIMEOUT)
    page.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
    
    # Сбор логов консоли
    console_logs = []
    def handle_console(msg):
        console_logs.append(f"[{msg.type}] {msg.text}")
    page.on("console", handle_console)
    
    yield page
    
    # Закрытие ресурсов после теста
    video_path = None
    if RECORD_VIDEO and page.video:
        video_path = page.video.path()
    
    if RECORD_TRACING:
        context.tracing.stop(path=f'./tracing/{test_name}.zip')
    
    context.close()
    browser.close()
    
    # Прикрепляем трейсинг к Allure
    if RECORD_TRACING:
        tracing_file = f'./tracing/{test_name}.zip'
        if os.path.exists(tracing_file):
            allure.attach.file(tracing_file, name='trace', extension='zip')
    
    # Прикрепляем видео к Allure
    if RECORD_VIDEO and video_path and os.path.exists(video_path):
        allure.attach.file(video_path, name='video', attachment_type=allure.attachment_type.WEBM)
    
    # Прикрепляем логи консоли к Allure
    log_content = "\n".join(console_logs) if console_logs else "No console logs captured."
    allure.attach(log_content, name="console_logs", attachment_type=allure.attachment_type.TEXT)