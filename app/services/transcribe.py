"""Утилиты для транскрибирования аудио."""

import tempfile
from typing import List, Optional
from pathlib import Path
from pydub import AudioSegment
from app.utils.logger import setup_logger
from app.utils import openai_client
from app.utils.temp_dir import cleanup_files
from app.utils.cancel import is_user_canceled
from app.database.models.user import User

logger = setup_logger(__name__)


async def whisper_inference(file_path: str | Path) -> str:
    """
    Транскрибирует аудиофайл с использованием API OpenAI Whisper.

    :param file_path: Путь к аудиофайлу.
    :return: Текст транскрипции.
    :raises: Исключение при ошибке транскрибирования.
    """
    try:
        with open(file_path, "rb") as audio_file:
            transcription = await openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        logger.info("Транскрипция файла %s выполнена успешно.", file_path)
        return transcription.text
    except Exception as e:
        logger.error("Ошибка при транскрипции аудио: %s", e, exc_info=True)
        raise


async def process_audio_segment(
    segment: AudioSegment,
    segment_index: int = 0
) -> str:
    """
    Обрабатывает отдельный сегмент аудио.

    :param segment: Сегмент аудио для обработки.
    :param segment_index: Индекс сегмента для логирования.
    :return: Транскрипция сегмента.
    """
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".mp3"
    ) as temp_file:
        try:
            segment.export(
                temp_file.name,
                format="mp3",
                bitrate="128k"
            )
            transcription = await whisper_inference(temp_file.name)
            logger.debug(
                "Сегмент %d успешно транскрибирован", segment_index
            )
            return transcription
        finally:
            cleanup_files(temp_file.name)


async def transcribe_audio(file_path: str | Path, user: User) -> Optional[str]:
    """
    Транскрибирует аудиофайл, разбив его на меньшие сегменты
    и объединив транскрипции.

    :param file_path: Путь к аудиофайлу.
    :param user: Пользователь.
    :return: Полный текст транскрипции.
    :raises: FileNotFoundError, Exception
    """
    try:
        if await is_user_canceled(user):
            return None

        audio = AudioSegment.from_file(file_path)
        audio = audio.set_frame_rate(16000)
        segment_length_ms = 25 * 60 * 1000

        if len(audio) <= segment_length_ms:
            return await process_audio_segment(audio)

        transcriptions: List[str] = []
        for i, start_ms in enumerate(
            range(0, len(audio), segment_length_ms)
        ):
            if await is_user_canceled(user):
                return None

            segment = audio[start_ms:start_ms + segment_length_ms]

            transcription = await process_audio_segment(segment, i)
            transcriptions.append(transcription)

        full_transcription = " ".join(transcriptions)
        logger.info("Полная транскрипция выполнена успешно.")
        return full_transcription if not await is_user_canceled(user) else None

    except FileNotFoundError:
        logger.error("Файл %s не найден.", file_path)
        raise
    except Exception as e:
        logger.error(
            "Ошибка при транскрипции большого аудиофайла: %s", e, exc_info=True
        )
        raise
