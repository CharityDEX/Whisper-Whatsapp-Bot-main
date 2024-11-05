"""Обработчик событий старта."""
from app.whapi.message import Message, MessageType
from app.whapi import whapi_client
from app.database.models.user import User
from app.database.state.user import UserState
from app.database.crud import CRUD
from app.utils.logger import setup_logger
from commands import START_COMMAND
from keyboards import start_keyboard
from messages import START_MESSAGE

logger = setup_logger(__name__)


async def send_welcome_message(user: User) -> None:
    """
    Отправка приветственного сообщения

    :param user: Пользователь
    """
    if user.state == UserState.START:
        crud = CRUD(User)
        await crud.update(user, state=None)

    await whapi_client.send_message(
        user.number, START_MESSAGE, markup=start_keyboard
    )


async def route(user: User, message: Message) -> bool:
    """
    Обработчик старта

    :param user: Пользователь
    :param message: Сообщение
    """
    if user.state == UserState.START:
        await send_welcome_message(user)
        return True

    if isinstance(message, Message):
        if (
            message.type == MessageType.TEXT
            and message.text.strip().lower() == START_COMMAND
        ):
            await send_welcome_message(user)
            return True
    return False
