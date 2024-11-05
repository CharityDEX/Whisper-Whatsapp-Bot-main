"""Конфигурация приложения."""
import os
import time
from typing import Optional
from dotenv import load_dotenv
from app.utils.logger import setup_logger


logger = setup_logger(__name__)


class Config:
    """Класс конфигурации."""

    def __init__(self, env_file: str) -> None:
        """
        Инициализация конфигурации путем загрузки переменных окружения.

        :param env_file: Путь к файлу .env.
        """
        self._load_environment_variables(env_file)
        self.whapi_token = self._get_env_variable("WHAPI_TOKEN")
        self.webhook_host = self._get_env_variable("WEBHOOK_HOST", 'localhost')
        self.admin_number = self._get_env_variable("ADMIN_NUMBER")
        self.timezone = self._get_env_variable("TIMEZONE", "UTC")
        self.openai_api_key = self._get_env_variable("OPENAI_API_KEY")
        self.proxy = self._get_env_variable("PROXY", 'localhost')
        os.environ['TZ'] = self.timezone
        time.tzset()
        self.database_url = (
            "sqlite+aiosqlite:///"
            + os.path.join(os.path.dirname(__file__), 'database')
            + f'/{self._get_env_variable("DATABASE_NAME")}'
        )

    def _load_environment_variables(self, env_file: str) -> None:
        """
        Загрузка переменных окружения из указанного файла .env.

        :param env_file: Путь к файлу .env.
        """
        try:
            load_dotenv(dotenv_path=env_file)
            logger.info("Переменные окружения загружены из %s", env_file)
        except Exception as e:
            logger.error("Ошибка загрузки %s: %s", env_file, e)

    def _get_env_variable(
        self,
        key: str,
        default: Optional[str] = None
    ) -> Optional[str]:
        """
        Получение значения переменной окружения с возможным значением по
        умолчанию.

        :param key: Ключ переменной окружения.
        :param default: Значение по умолчанию, если ключ не найден.

        :return: Значение переменной окружения или значение по умолчанию.
        """
        value = os.getenv(key, default)
        if value is None:
            logger.warning(
                "%s is not set. Using default: %s", key, default
            )
        return value

    def _get_int_env_variable(
        self,
        key: str,
        default: int = 0
    ) -> int:
        """
        Получение целочисленного значения переменной окружения с
        значением по умолчанию.

        :param key: Ключ переменной окружения.
        :param default: Значение по умолчанию, если ключ не найден.

        :return: Целочисленное значение переменной окружения или значение
        по умолчанию.
        """
        try:
            return int(self._get_env_variable(key, str(default)))
        except ValueError:
            logger.error(
                "Неверное значение для %s, используется значение по "
                "умолчанию: %s", key, default
            )
            return default


# Загрузка переменных окружения
config = Config(os.path.join(os.path.dirname(__file__), '.env'))
