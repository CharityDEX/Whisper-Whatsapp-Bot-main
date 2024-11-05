"""Обработчик событий отмены."""
from typing import Union
from app.whapi.message import ReplyMessage
from app.whapi import whapi_client
from app.database.models.user import User
from app.database.crud import CRUD
from app.utils.logger import setup_logger
from messages import CANCEL_MESSAGE
from keyboards import CANCEL_ID, new_audio_keyboard

logger = setup_logger(__name__)


async def cancel_handler(user: User) -> None:
    """
    Отправка сообщения с отменой действия

    :param user: Пользователь
    """
    crud = CRUD(User)
    await crud.update(user, state=None)
    await whapi_client.send_message(
        user.number, CANCEL_MESSAGE, markup=new_audio_keyboard
    )


async def route(user: User, message: Union[ReplyMessage]) -> bool:
    """
    Обработчик сообщения с отменой действия

    :param user: Пользователь
    :param message: Сообщение
    """

    if isinstance(message, ReplyMessage) and message.button_id == CANCEL_ID:
        await cancel_handler(user)
        return True
    return False
