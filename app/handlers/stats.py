"""Обработчик событий статистики."""
from typing import Dict
from sqlalchemy import select, func
from app.database.engine import async_session_factory
from app.database.models.user import User
from app.whapi import whapi_client
from app.whapi.message import Message, MessageType
from app.utils.logger import setup_logger
from messages import STATS_MESSAGE
from commands import STATS_COMMAND

logger = setup_logger(__name__)


async def get_stats() -> Dict[str, int]:
    """
    Получает статистику пользователей.

    :return: Статистика пользователей
    """
    async with async_session_factory() as session:
        registered_users = await session.scalar(
            select(func.count(User.number))
        )
        today = await session.scalar(
            select(func.current_date())
        )
        new_users = await session.scalar(
            select(func.count(User.number)).where(
                func.date(User.created_at) == today
            )
        )
        uploaded_audios = await session.scalar(
            select(func.sum(User.uploaded_audios))
        )
        gpt_requests = await session.scalar(
            select(func.sum(User.gpt_requests))
        )

    return {
        "registered_users": registered_users,
        "new_users": new_users,
        "uploaded_audios": uploaded_audios,
        "gpt_requests": gpt_requests
    }


async def send_stats_message(user: User) -> None:
    """
    Отправка сообщения с статистикой

    :param user: Пользователь
    """
    stats = await get_stats()
    await whapi_client.send_message(user.number, STATS_MESSAGE.format(**stats))


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
                and message.text.strip().lower() == STATS_COMMAND
            ):
                await send_stats_message(user)
                return True
    return False
