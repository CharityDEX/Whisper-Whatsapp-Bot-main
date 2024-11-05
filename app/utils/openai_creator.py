"""OpenAI конфигуратор."""
import httpx
from openai import AsyncOpenAI, OpenAIError
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class OpenAICreator:
    """Конфигуратор OpenAI."""

    @staticmethod
    def create_openai_client(api_key: str, proxy: str) -> AsyncOpenAI:
        """
        Создает клиента OpenAI с настройками прокси и тайм-аута.

        :return: Настроенный клиент OpenAI.
        :raises: OpenAIError, если не удалось создать клиента.
        """
        proxies = (
            None if proxy == 'localhost'
            else {'https://': proxy, 'http://': proxy}
        )
        logger.info(
            "Прокси не используется (указан localhost)."
            if proxies is None else f"Используется прокси: {proxy}"
        )

        try:
            client = AsyncOpenAI(
                api_key=api_key,
                http_client=httpx.AsyncClient(proxies=proxies, timeout=360)
            )
            logger.info("Клиент OpenAI успешно инициализирован.")
            return client
        except OpenAIError as e:
            logger.error("Не удалось инициализировать клиент OpenAI: %s", e)
            raise
