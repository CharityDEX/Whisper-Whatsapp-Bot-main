"""Установка маршрутов."""
from typing import Union
from app.database.models.user import User
from app.whapi.message import Message, MediaMessage, ReplyMessage
from . import (
    start, support, cancel, new_audio, stats, admin, process, question
)


async def handler_routing(
    user: User,
    message: Union[Message, MediaMessage, ReplyMessage]
) -> None:
    """Обработчик маршрутизации"""
    routes = [
        start.route,
        support.route,
        cancel.route,
        new_audio.route,
        stats.route,
        admin.route,
        process.route,
        question.route
    ]

    for route in routes:
        if await route(user, message):
            return
