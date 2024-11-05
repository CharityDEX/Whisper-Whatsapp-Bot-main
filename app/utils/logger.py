"""Настройка логгера."""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler


def setup_logger(
    name: str,
    log_file: str = 'log.txt',
    log_dir: str = 'logs',
    level: int = logging.INFO
) -> logging.Logger:
    """
    Настройка и возврат логгера.

    :param name: имя логгера
    :param log_file: путь к файлу логов
    :param level: уровень логирования
    :return: объект логгера
    """
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, log_file)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    file_handler = RotatingFileHandler(
        log_file, maxBytes=5*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False
    return logger
