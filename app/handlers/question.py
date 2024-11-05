"""Обработчик событий вопроса."""
from app.whapi.message import Message, MessageType
from app.whapi import whapi_client
from app.database.models.user import User
from app.database.crud import CRUD
from app.services.question import get_answer
from app.utils.logger import setup_logger
from keyboards import new_audio_keyboard
from messages import (
    WITHOUT_TRANSCRIPTION_MESSAGE,
    RESPONSE_GENERATION_MESSAGE,
    ERROR_RESPONSE_GENERATION_MESSAGE
)

logger = setup_logger(__name__)


async def question_handler(user: User, message: Message) -> None:
    """
    Обработчик сообщения с вопросом.

    :param user: Пользователь
    :param message: Сообщение
    """
    if not user.last_transcription_text:
        await whapi_client.send_message(
            user.number,
            WITHOUT_TRANSCRIPTION_MESSAGE,
            markup=new_audio_keyboard
        )
        return

    await whapi_client.send_message(
        user.number,
        RESPONSE_GENERATION_MESSAGE
    )

    try:
        answer = await get_answer(user.last_transcription_text, message.text)
        crud = CRUD(User)
        await crud.update(user, gpt_requests=user.gpt_requests + 1)
    except Exception as e:
        logger.error("Произошла ошибка при генерации ответа: %s", e)
        answer = ERROR_RESPONSE_GENERATION_MESSAGE

    await whapi_client.send_message(
        user.number, answer, markup=new_audio_keyboard
    )
    logger.info("Ответ на вопрос отправлен пользователю %s", user.number)


async def route(user: User, message: Message) -> bool:
    """
    Маршрутизация сообщения к соответствующему обработчику.

    :param user: Пользователь
    :param message: Сообщение
    :return: Булевое значение, указывающее, было ли сообщение обработано
    """
    if isinstance(message, Message) and message.type == MessageType.TEXT:
        await question_handler(user, message)
        return True
    return False
