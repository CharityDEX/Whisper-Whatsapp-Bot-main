"""Менеджер URL."""
from typing import Optional
import aiohttp
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class URLManager:
    """Класс для управления URL."""

    def __init__(self, host: str) -> None:
        """
        Инициализация класса.

        :param host: Хост.
        """
        self.host = host

    @classmethod
    async def create(cls, host: str) -> 'URLManager':
        """
        Асинхронная инициализация.

        :return: Экземпляр класса.
        """
        self = cls(host)
        self.host = await self._create_base_url()
        return self

    async def _get_external_ip(self) -> Optional[str]:
        """
        Получает внешний IP-адрес через myip.

        :return: Внешний IP-адрес в виде строки, если успешен запрос, иначе
        None.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    'https://api.myip.com/', timeout=10
                ) as response:
                    response.raise_for_status()
                    data = await response.json(content_type='text/html')
                    ip = data.get('ip')
                    logger.info("Внешний IP: %s", ip)
                    return ip
        except aiohttp.ClientError as e:
            logger.error("Не удалось получить внешний IP: %s", e)
            return None

    async def _create_base_url(self) -> Optional[str]:
        """Создать базовый URL."""
        if not self.host:
            raise ValueError(
                "Базовый URL не может быть None или пустой строкой."
            )
        try:
            # Создание локального webhook URL
            if self.host == 'localhost':
                external_ip = await self._get_external_ip()
                if not external_ip:
                    logger.error(
                        "Не удалось получить внешний IP для локального хоста.")
                    return None
                url = f'http://{external_ip}:7729'
                logger.info("Создан локальный URL: %s", url)
            else:
                # Создание внешнего webhook URL
                url = self.host.rstrip("/")
                logger.info("Создан внешний URL: %s", url)
            return url

        except Exception as e:
            logger.error(
                "Ошибка при создании webhook URL: %s", str(e),
                exc_info=True
            )
            return None

    def get_webhook_url(self) -> Optional[str]:
        """Получить URL вебхука."""
        return self.host + '/webhook'
