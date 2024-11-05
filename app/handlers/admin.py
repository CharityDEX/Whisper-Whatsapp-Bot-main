"""Обработчик событий установки и удаления администратора."""
from app.database.crud import CRUD
from app.database.models.user import User
from app.whapi import whapi_client
from app.whapi.message import Message, MessageType
from app.utils.logger import setup_logger
from config import config
from commands import ADMIN_COMMAND
from messages import (
    USER_NOT_FOUND_MESSAGE,
    SET_ADMIN_MESSAGE,
    UNSET_ADMIN_MESSAGE,
    ADMIN_COMMAND_HELP_MESSAGE,
    NOT_CHANGE_ADMIN_MESSAGE
)

logger = setup_logger(__name__)


async def set_or_unset_admin(user: User, message: Message) -> None:
    """
    Устанавливает пользователя в качестве администратора

    :param message: Сообщение
    """
    try:
        _, action, number = message.text.strip().lower().split()
        number = int(number)
        if action not in ['set', 'unset']:
            raise ValueError
    except (ValueError, IndexError):
        logger.error("Неверный формат команды администратора")
        await whapi_client.send_message(
            user.number, ADMIN_COMMAND_HELP_MESSAGE
        )
        return

    crud = CRUD(User)
    target_user = await crud.get(number=number)
    if target_user:
        if target_user.number == config.admin_number:
            await whapi_client.send_message(
                user.number, NOT_CHANGE_ADMIN_MESSAGE.format(number=number)
            )
            return
        await crud.update(target_user, is_admin=(action == 'set'))
        msg = (
            SET_ADMIN_MESSAGE if action == 'set'
            else UNSET_ADMIN_MESSAGE
        ).format(number=number)
        await whapi_client.send_message(user.number, msg)

        logger.info(
            "Пользователь %s %s в качестве администратора",
            number, "установлен" if action == 'set' else "удален"
        )
    else:
        logger.error('Пользователь %s не найден', number)
        await whapi_client.send_message(
            user.number, USER_NOT_FOUND_MESSAGE.format(number=number)
        )


async def route(user: User, message: Message) -> None:
    """
    Обработчик сообщения с запросом статистики

    :param user: Пользователь
    :param message: Сообщение
    """
    if isinstance(message, Message):
        if user.is_admin:
            if (
                message.type == MessageType.TEXT
                and message.text.strip().lower().startswith(ADMIN_COMMAND)
            ):
                await set_or_unset_admin(user, message)
                return True
    return False
