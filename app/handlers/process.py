"""Обработчик событий процесса."""
from typing import Tuple
from app.whapi.message import MediaMessage
from app.whapi import whapi_client
from app.database.models.user import User
from app.database.state.user import UserState
from app.database.crud import CRUD
from app.filters.mime_type import MIME_TYPE_FILTER
from app.filters import in_process_filter
from app.utils.logger import setup_logger
from app.services.transcribe import transcribe_audio
from app.services.summarize import summarize_text
from app.utils.cancel import is_user_canceled
from app.utils.temp_dir import (
    download_media,
    cleanup_files,
    save_transcription_as_text
)
from keyboards import new_audio_keyboard
from messages import (
    IN_PROCESS_MESSAGE,
    SUMMARY_MESSAGE,
    TRANSCRIPTION_MESSAGE,
    ALREADY_IN_PROCESS_MESSAGE,
    ERROR_IN_PROCESS_MESSAGE
)


logger = setup_logger(__name__)

TRANSCRIPTION_FILENAME = "transcription.txt"


async def update_user_data(
    user: User,
    transcription: str,
    summary: str
) -> None:
    """
    Обновляет данные пользователя в базе данных.

    :param user: Пользователь.
    :param transcription: Транскрибированный текст.
    :param summary: Суммаризированный текст.
    """
    crud = CRUD(User)
    await crud.update(
        user,
        state=None,
        last_transcription_text=transcription,
        last_summary_text=summary,
        uploaded_audios=user.uploaded_audios + 1,
    )


async def process_media(media_url: str, user: User) -> Tuple[str, str]:
    """
    Обрабатывает медиафайл: конвертирует, транскрибирует и суммирует.

    :param media_url: URL медиафайла.
    :param user: Пользователь.
    :return: Транскрибированный и суммаризированный текст.
    :raises: Исключение при ошибке обработки медиа.
    """
    try:
        logger.info("Обработка медиа для пользователя %s", user.number)
        audio_path = await download_media(media_url)
        transcription = await transcribe_audio(audio_path, user)
        summary = await summarize_text(transcription, user)

        if transcription and summary and not await is_user_canceled(user):
            await update_user_data(user, transcription, summary)
            await handle_transcription_and_summary(
                user, transcription, summary
            )
            return transcription, summary
        logger.error("Транскрипция или суммаризация отменена")
    except FileNotFoundError as e:
        logger.error("Файл не найден: %s", e, exc_info=True)
        raise
    except Exception as e:
        logger.error("Ошибка в процессе обработки медиа: %s", e, exc_info=True)
        raise
    finally:
        cleanup_files(audio_path)


async def handle_transcription_and_summary(
    user: User,
    transcription: str,
    summary: str
) -> None:
    """
    Обрабатывает отправку транскрипции и суммы пользователю.

    :param user: Пользователь.
    :param transcription: Транскрибированный текст.
    :param summary: Суммаризированный текст.
    """
    transcription_file_path = save_transcription_as_text(transcription)
    await whapi_client.send_document(
        user.number,
        TRANSCRIPTION_FILENAME,
        transcription_file_path,
        caption=TRANSCRIPTION_MESSAGE
    )
    await whapi_client.send_message(
        user.number,
        SUMMARY_MESSAGE.format(summary=summary),
        markup=new_audio_keyboard
    )
    cleanup_files(transcription_file_path)


async def start_process(user: User, message: MediaMessage) -> None:
    """
    Обработка медиа сообщения

    :param user: Пользователь
    :param message: Медиа сообщение
    """
    try:
        in_process_filter.add_user(user.number)
        await whapi_client.send_message(user.number, IN_PROCESS_MESSAGE)
        await process_media(message.link, user)
    except Exception as e:
        logger.error("Ошибка в процессе обработки медиа: %s", e, exc_info=True)
        await whapi_client.send_message(
            user.number,
            ERROR_IN_PROCESS_MESSAGE,
            markup=new_audio_keyboard
        )
    finally:
        in_process_filter.remove_user(user.number)


async def already_in_process(user: User) -> None:
    """
    Отправляет сообщение о том, что пользователь уже обрабатывает аудио.
    """
    await whapi_client.send_message(user.number, ALREADY_IN_PROCESS_MESSAGE)


async def route(user: User, message: MediaMessage) -> bool:
    """
    Обработчик медиа сообщений

    :param user: Пользователь
    :param message: Медиа сообщение
    """
    if in_process_filter.user_exists(user.number):
        await already_in_process(user)
        return True

    if isinstance(message, MediaMessage):
        if (
            message.mime_type in MIME_TYPE_FILTER
            and user.state == UserState.NEW_AUDIO
            and not in_process_filter.user_exists(user.number)
        ):
            await start_process(user, message)
            return True
    return False
