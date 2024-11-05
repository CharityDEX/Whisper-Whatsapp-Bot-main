"""Модуль middleware для обработки запросов."""
from typing import Union
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from app.handlers import handler_routing
from app.utils.logger import setup_logger
from app.whapi.user import User as WAUser
from app.whapi.message import Message, MediaMessage, ReplyMessage
from app.database.crud import CRUD
from app.database.models.user import User
from app.database.state.user import UserState
from config import config


logger = setup_logger(__name__)


async def middleware(body: dict) -> None:
    """
    Middleware для обработки событий

    :param body: Вебхук
    """
    message_dict = body.get('messages', [])[0]
    if not message_dict:
        logger.warning("Отсутствует сообщение в вебхуке")
        return
    if message_dict.get('from_me'):
        return

    try:
        wa_user = _get_wa_user(message_dict)
        message = _get_message(message_dict)
        if not message:
            return

        user = await _ensure_user_in_db(wa_user)
        await handler_routing(user, message)
    except SQLAlchemyError as e:
        logger.error("Ошибка при работе с базой данных: %s", e, exc_info=True)
        raise
    except Exception as e:
        logger.error("Ошибка в middleware: %s", e, exc_info=True)
        raise


async def _ensure_user_in_db(wa_user: WAUser) -> User:
    """
    Гарантирует, что пользователь зарегистрирован в базе данных.

    :param wp_user: Пользователь WhatsApp
    :return: Пользователь
    """
    user_crud = CRUD(User)
    try:
        user = await user_crud.get(wa_user.number)

        user_data = {
            'name': wa_user.from_name,
            'updated_at': func.now()
        }

        if not user:
            user = await user_crud.create(
                number=wa_user.number,
                is_admin=wa_user.number == config.admin_number,
                state=UserState.START,
                **user_data
            )
            logger.info("%s зарегистрирован в базе данных.", wa_user.number)
        else:
            user = await user_crud.update(user, **user_data)
            logger.info("%s обновлен в базе данных.", wa_user.number)

        return user
    except SQLAlchemyError as e:
        logger.error("Ошибка при работе с базой данных: %s", e, exc_info=True)
        raise


def _get_wa_user(message_dict) -> WAUser:
    """Получение пользователя WhatsApp

    :param message_dict: Вебхук
    :return: Пользователь WhatsApp
    """
    wa_user = WAUser(
        number=message_dict.get('from'),
        chat_id=message_dict.get('chat_id'),
        source=message_dict.get('source'),
        from_name=message_dict.get('from_name')
    )
    return wa_user


def _get_message(
    message_dict: dict
) -> Union[Message, MediaMessage, ReplyMessage]:
    """Получение сообщения

    :param message_dict: Вебхук
    :return: Сообщение
    """
    message_type = message_dict.get('type')
    if not message_type:
        logger.warning("Отсутствует тип сообщения в теле запроса")
        return

    timestamp = message_dict.get('timestamp')

    if message_type == 'text':
        return Message.create(message_dict, timestamp)
    elif message_type in {'voice', 'audio', 'document', 'video'}:
        return MediaMessage.create(message_dict, message_type, timestamp)
    elif message_type == 'reply':
        return ReplyMessage.create(message_dict, timestamp)

    logger.warning("Неподдерживаемый тип сообщения: %s", message_type)
