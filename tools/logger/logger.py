import logging
import re

# Единый handler для всех логгеров
_file_handler = None


class CallLogFilter(logging.Filter):
    """Фильтрует Call log из сообщений Playwright-исключений"""
    def filter(self, record):
        if record.msg and "Call log:" in str(record.msg):
            record.msg = re.split(r'\nCall log:', str(record.msg))[0]
        return True


def get_logger(name: str) -> logging.Logger:
    global _file_handler
    
    logger = logging.getLogger(name)
    
    # Проверяем, настроен ли уже этот логгер
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # Создаём единый file handler только один раз
    if _file_handler is None:
        _file_handler = logging.FileHandler("Log.log", mode='w', encoding='utf-8')
        _file_handler.setLevel(logging.DEBUG)
        _file_handler.addFilter(CallLogFilter())
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        _file_handler.setFormatter(formatter)
    
    logger.addHandler(_file_handler)
    return logger