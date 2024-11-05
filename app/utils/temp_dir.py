"""Утилиты для работы с временными файлами."""
import os
import tempfile
from app.utils.logger import setup_logger
from app.whapi import whapi_client

logger = setup_logger(__name__)


async def download_media(media_url: str) -> str:
    """
    Скачивает медиафайл и сохраняет его во временную директорию.

    :param media_url: URL медиафайла.
    :return: Путь к скачанному временному файлу.
    :raises: Исключение при ошибке скачивания.
    """

    response = await whapi_client.get_file(media_url)

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(response)
        temp_file_path = temp_file.name
        logger.info(
            "Медиафайл %s скачан во временный файл %s",
            media_url, temp_file_path
        )
    return temp_file_path


def cleanup_files(*file_paths: str) -> None:
    """
    Удаляет временные файлы.

    :param file_paths: Пути к временным файлам для удаления.
    """
    for file_path in file_paths:
        try:
            os.remove(file_path)
            logger.info("Файл %s удален.", file_path)
        except OSError as e:
            logger.error(
                "Ошибка при удалении файла %s: %s", file_path, e, exc_info=True
            )


def save_transcription_as_text(transcription: str) -> str:
    """
    Сохраняет транскрипцию в текстовый файл.

    :param transcription: текст транскрипции
    :return: полный путь к файлу
    """
    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".txt", mode='w', encoding='utf-8'
        ) as text_file:
            text_file.write(transcription)
            filename = text_file.name

        logger.info("Текстовый файл сохранен как %s", filename)
        return filename
    except Exception as e:
        logger.error(
            "Ошибка сохранения текстового файла: %s", e, exc_info=True
        )
        raise
