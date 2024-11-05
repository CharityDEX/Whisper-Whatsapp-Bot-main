"""Модуль для работы с данными сообщения WHAPI."""
from dataclasses import dataclass
from typing import Optional


class MessageType:
    """Типы сообщений."""
    TEXT = 'text'
    REPLY = 'reply'


@dataclass
class Message:
    """Базовый класс сообщения."""
    id: str
    type: str
    text: Optional[str]
    timestamp: int

    @classmethod
    def create(cls, message_dict: dict, timestamp: int) -> 'Message':
        """
        Создать текстовое сообщение из данных вебхука.

        :param message_dict: Данные вебхука.
        :param timestamp: Время отправки сообщения.
        :return: Текстовое сообщение.
        """
        return cls(
            id=message_dict.get('id'),
            type=MessageType.TEXT,
            text=message_dict.get('text', {}).get('body'),
            timestamp=timestamp
        )


@dataclass
class MediaMessage(Message):
    """Класс медиа сообщения."""
    file_id: str
    link: str
    file_name: str
    mime_type: str

    @classmethod
    def create(
        cls,
        message_dict: dict,
        message_type: str,
        timestamp: int
    ) -> 'MediaMessage':
        """
        Создать медиа сообщение из данных вебхука.

        :param message_dict: Данные вебхука.
        :param message_type: Тип сообщения.
        :param timestamp: Время отправки сообщения.
        :return: Медиа сообщение.
        """
        media_data = message_dict.get(message_type, {})
        return cls(
            id=message_dict.get('id'),
            type=message_type,
            text=media_data.get('caption'),
            timestamp=timestamp,
            file_id=media_data.get('id'),
            link=media_data.get('link'),
            file_name=media_data.get('file_name'),
            mime_type=media_data.get('mime_type')
        )


@dataclass
class ReplyMessage(Message):
    """Класс быстрой кнопки."""
    button_id: str

    @classmethod
    def create(
        cls,
        message_dict: dict,
        timestamp: int
    ) -> 'ReplyMessage':
        """
        Создать сообщение с быстрой кнопкой из данных вебхука.

        :param message_dict: Данные вебхука.
        :param timestamp: Время отправки сообщения.
        :return: Сообщение с быстрой кнопкой.
        """
        reply_data = message_dict.get('reply', {}).get('buttons_reply', {})
        button_id = reply_data.get('id', '').split(':')[1]
        return cls(
            id=message_dict.get('id'),
            type=MessageType.REPLY,
            text=None,
            timestamp=timestamp,
            button_id=button_id
        )
