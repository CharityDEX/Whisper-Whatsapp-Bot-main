"""Обработчик событий поддержки."""
from typing import Union
from app.whapi.message import Message, ReplyMessage, MessageType
from app.whapi import whapi_client
from app.database.models.user import User
from app.utils.logger import setup_logger
from commands import SUPPORT_COMMAND
from messages import SUPPORT_MESSAGE
from keyboards import SUPPORT_ID


logger = setup_logger(__name__)


async def send_support_message(user: User) -> None:
    """
    Отправка сообщения с контактами поддержки

    :param user: Пользователь
    """
    await whapi_client.send_message(user.number, SUPPORT_MESSAGE)


async def route(user: User, message: Union[Message, ReplyMessage]) -> bool:
    """
    Обработчик сообщения с контактами поддержки

    :param user: Пользователь
    :param message: Сообщение
    """
    async def should_send_support_message(
        message: Union[Message, ReplyMessage]
    ) -> bool:
        if (
            message.type == MessageType.TEXT
            and message.text.strip().lower() == SUPPORT_COMMAND
        ):
            return True
        if (
            message.type == MessageType.REPLY
            and message.button_id == SUPPORT_ID
        ):
            return True
        return False

    if isinstance(
        message, (Message, ReplyMessage)
    ) and await should_send_support_message(message):
        await send_support_message(user)
        return True
    return False
