import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Конфигурация логгера который должен писаться в файл и в консоль

LOG_BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(LOG_BASE_PATH, exist_ok=True)

# Получение объекта логгера для приложения app1
logger = logging.getLogger('abcp_parser')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = TimedRotatingFileHandler(
    os.path.join(LOG_BASE_PATH, 'abcp_parser.log'),
    when='W0',  # Запуск ротации каждую неделю (W0 - начало недели)
    interval=1,  # Интервал в неделях
    backupCount=5  # Хранить последние 5 архивных файлов
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

logger.addHandler(file_handler)