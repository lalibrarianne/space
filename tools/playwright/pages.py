import os
import shutil
from typing import Generator

import allure
from playwright.sync_api import Playwright, Page
from dotenv import load_dotenv
from io import StringIO


load_dotenv()
# Add download directory configuration
DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', os.getcwd()) 

#Browser configuration
SLOW_MO = int(os.getenv('SLOW_MO', '0'))  
HEADLESS = os.getenv('HEADLESS', 'true').lower() == 'true'
RECORD_VIDEO = os.getenv('RECORD_VIDEO', 'false').lower() == 'true'
RECORD_TRACING = os.getenv('RECORD_TRACING', 'false').lower() == 'true'
BROWSERS_CONFIG = StringIO(os.getenv('BROWSERS', ''))
browser_channel = os.getenv('BROWSER_CHANNEL')

# Timeout configurations (in milliseconds)
DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT'))  
NAVIGATION_TIMEOUT = int(os.getenv('NAVIGATION_TIMEOUT')) 
ACTION_TIMEOUT = int(os.getenv('ACTION_TIMEOUT'))  
BROWSER_LAUNCH_TIMEOUT = int(os.getenv('BROWSER_LAUNCH_TIMEOUT'))  

def initialize_playwright_page(
        playwright: Playwright,
        test_name: str,
        browser_type: str,
        storage_state: str | None = None,
        download_dir: str | None = None) -> Generator[Page, None, None]:
    
    actual_download_dir = download_dir or DOWNLOAD_DIR
    os.makedirs(actual_download_dir, exist_ok=True)
    # Create folders only if recording is enabled
    if RECORD_VIDEO:
        os.makedirs('./videos', exist_ok=True)
    if RECORD_TRACING:
        os.makedirs('./tracing', exist_ok=True)
    
    # Configure context options with download settings
    context_options = {
        'storage_state': storage_state,
        'viewport': {'width': 1280, 'height': 720},
        'accept_downloads': True,  # Enable downloads
    }

    
    # Add video recording if enabled
    if RECORD_VIDEO:
        context_options['record_video_dir'] = './videos'
        context_options['record_video_size'] = {"width": 1280, "height": 720}

    launch_args = {
        'headless': HEADLESS,
        'timeout': BROWSER_LAUNCH_TIMEOUT,
        'slow_mo': SLOW_MO,
        'args': [
            # "--disable-beforeunload-dialogs",
            # "--disable-dev-shm-usage",
            # "--disable-features=TranslateUI",
            # "--disable-hang-monitor",
            # "--disable-ipc-flooding-protection",
            # "--disable-notifications",
            # "--disable-prompt-on-repost",
            # "--disable-renderer-backgrounding",
            # "--disable-site-isolation-trials",
            # "--disable-web-security",
            # "--automatic-downloads=1",
            # "--no-default-browser-check",
            # "--no-first-run",
            # "--disable-component-extensions-with-background-pages",
            # "--disable-default-apps",
            # "--disable-extensions-file-access-check",
            # "--disable-extensions-http-throttling",
            # "--disable-extensions",
            # "--disable-file-system",
            # "--disable-plugins-discovery",
            # "--disable-translate",
            # "--disable-background-timer-throttling",
            # "--disable-backgrounding-occluded-windows",
            # "--disable-renderer-backgrounding",
            # "--disable-external-protocol-dialog", 
            # "--no-default-browser-check",
            # "--disable-component-update", 
        ]
    }

    if browser_channel:
        launch_args['channel'] = browser_channel
    
    browser = playwright[browser_type].launch(**launch_args)
    context = browser.new_context(**context_options)
    
    # Set default timeouts for the context
    context.set_default_timeout(DEFAULT_TIMEOUT)
    context.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
    
    # Start tracing only if enabled
    if RECORD_TRACING:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    page = context.new_page()
    
    # Set page-level timeouts (these override context timeouts for this specific page)
    page.set_default_timeout(ACTION_TIMEOUT)
    page.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
    
    # mock_static_resources(page)
    
    # Set up console log capturing
    console_logs = []
    def handle_console(msg):
        console_logs.append(f"[{msg.type}] {msg.text}")

    page.on("console", handle_console)


    yield page

    # After test: Stop tracing and close resources
    video_path = None
    if RECORD_VIDEO and page.video:
        video_path = page.video.path()
    
    if RECORD_TRACING:
        context.tracing.stop(path=f'./tracing/{test_name}.zip')
    
    context.close()
    browser.close()

    # Attach tracing if enabled and file exists
    if RECORD_TRACING:
        tracing_file = f'./tracing/{test_name}.zip'
        if os.path.exists(tracing_file):
            allure.attach.file(tracing_file, name='trace', extension='zip')

    # Attach video if enabled and file exists
    if RECORD_VIDEO and video_path and os.path.exists(video_path):
        allure.attach.file(video_path, name='video', attachment_type=allure.attachment_type.WEBM)
    elif RECORD_VIDEO and video_path:
        print(f"Warning: Video file not found at {video_path}")

    # Always attach console logs
    log_content = "\n".join(console_logs) if console_logs else "No console logs captured."
    allure.attach(log_content, name="console_logs", attachment_type=allure.attachment_type.TEXT)

