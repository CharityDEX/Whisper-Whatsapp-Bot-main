"""Обработчик событий нового аудио."""
from typing import Union
from app.whapi.message import Message, ReplyMessage, MessageType
from app.whapi import whapi_client
from app.database.models.user import User
from app.database.state.user import UserState
from app.database.crud import CRUD
from app.utils.logger import setup_logger
from messages import NEW_AUDIO_MESSAGE
from commands import NEW_AUDIO_COMMAND
from keyboards import NEW_AUDIO_ID, cancel_keyboard

logger = setup_logger(__name__)


async def send_new_audio_message(user: User) -> None:
    """
    Отправка сообщения с нового аудио

    :param user: Пользователь
    """
    crud = CRUD(User)
    await crud.update(user, state=UserState.NEW_AUDIO)
    await whapi_client.send_message(
        user.number, NEW_AUDIO_MESSAGE, markup=cancel_keyboard
    )


async def route(user: User, message: Union[Message, ReplyMessage]) -> bool:
    """
    Обработчик сообщения с контактами поддержки

    :param user: Пользователь
    :param message: Сообщение
    """
    async def should_send_new_audio_message(
        message: Union[Message, ReplyMessage]
    ) -> bool:
        if (
            message.type == MessageType.TEXT
            and message.text.strip().lower() == NEW_AUDIO_COMMAND
        ):
            return True
        if (
            message.type == MessageType.REPLY
            and message.button_id == NEW_AUDIO_ID
        ):
            return True
        return False

    if isinstance(
        message, (Message, ReplyMessage)
    ) and await should_send_new_audio_message(message):
        await send_new_audio_message(user)
        return True
    return False
