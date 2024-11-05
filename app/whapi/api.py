"""WHAPI API модуль."""
import random
import string
import base64
from typing import Dict, Any

import aiohttp

from app.utils.logger import setup_logger
from .buttons import Markup


logger = setup_logger(__name__)


class WHAPI:
    """Класс для работы с WHAPI."""

    def __init__(self, api_key: str) -> None:
        """
        Инициализация WHAPI.

        :param api_key: WHAPI API ключ.
        """
        self.api_key = api_key
        self._headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        self._base_url = 'https://gate.whapi.cloud'
        self.authorization_token = self._generate_authorization_token()

    async def _request(
        self,
        method: str,
        endpoint: str,
        json: Dict[str, Any],
    ) -> Any:
        """
        Делает HTTP запрос.

        :param method: HTTP метод (например, 'POST', 'PATCH').
        :param endpoint: API точка входа.
        :param json: JSON тело запроса.
        :return: JSON ответ.
        """
        url = f"{self._base_url}{endpoint}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method, url, headers=self._headers, json=json
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            logger.error("Ошибка HTTP запроса: %s", e)
            raise

    def _generate_authorization_token(self) -> str:
        """
        Генерация токена авторизации

        :return: Токен
        """
        return ''.join(
            random.choices(string.ascii_letters + string.digits, k=32)
        )

    async def send_message(
        self,
        to: str,
        message: str,
        markup: Markup | None = None
    ) -> dict:
        """
        Отправка сообщения через WHAPI.

        :param to: Номер телефона в формате.
        :param message: Текст сообщения.
        :param markup: Разметка.
        :return: JSON ответ.
        """
        body = {
            "to": str(to),
            "body": message,
            "typing_time": 0,
        }
        endpoint = '/messages/text'
        if markup:
            body = {
                "type": "button",
                "to": str(to),
                "body": {
                    "text": message
                },
                "action": markup.to_dict()
            }
            endpoint = '/messages/interactive'
        return await self._request('POST', endpoint, body)

    async def set_webhook(self, webhook_url: str) -> dict:
        """
        Установка вебхука.

        :param webhook_url: URL вебхука.
        :return: JSON ответ.
        """
        body = {
            "media": {
                "auto_download": [
                    "document",
                    "audio",
                    "video",
                    "voice"
                ],
            },
            "webhooks": [
                {
                    "headers": {
                        "Authorization": f"Bearer {self.authorization_token}"
                    },
                    "url": webhook_url,
                    "events": [{"type": "messages", "method": "post"}],
                    "mode": "body"
                }
            ]
        }
        response = await self._request('PATCH', '/settings', body)
        logger.info(
            "Webhook установлен: %s, авторизационный токен: %s",
            webhook_url, self.authorization_token
        )
        return response

    async def send_document(
        self,
        to: str,
        filename: str,
        file_path: str,
        caption: str,
    ) -> dict:
        """
        Отправка документа через WHAPI.

        :param to: Номер телефона в формате.
        :param filename: Имя файла.
        :param file_path: Путь к файлу.
        :param caption: Подпись.
        :return: JSON ответ.
        """
        base64_file = base64.b64encode(open(file_path, 'rb').read()).decode()
        body = {
            "to": str(to),
            "media": (
                "data:application/octet-stream;"
                f"name={filename};"
                f"base64,{base64_file}"
            ),
            "caption": caption
        }
        return await self._request('POST', '/messages/document', body)

    async def delete_message(self, message_id: str) -> dict:
        """
        Удаление сообщения.

        :param message_id: ID сообщения.
        :return: JSON ответ.
        """
        return await self._request('DELETE', f'/messages/{message_id}', None)

    async def get_file(self, link: str) -> bytes:
        """
        Получение файла.

        :param file_id: ID файла.
        :return: Содержимое файла.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as response:
                    response.raise_for_status()
                    return await response.read()
        except aiohttp.ClientError as e:
            logger.error("Ошибка HTTP запроса: %s", e)
            raise
