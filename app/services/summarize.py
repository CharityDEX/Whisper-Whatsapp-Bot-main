"""Утилиты для суммаризации текста."""
from typing import Optional
from app.utils import openai_client
from app.utils.logger import setup_logger
from app.database.models.user import User
from app.utils.cancel import is_user_canceled
from prompts import SUMMARY_PROMPT

logger = setup_logger(__name__)


async def summarize_text(text: str, user: User) -> Optional[str]:
    """
    Суммирует текст с использованием GPT-4o.

    :param text: Исходный текст для суммаризации.
    :param user: Пользователь.
    :return: Суммаризированный текст.
    :raises: Исключение при ошибке суммаризации текста.
    """
    try:
        if await is_user_canceled(user):
            return None

        completion = await openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SUMMARY_PROMPT},
                {"role": "user", "content": text}
            ]
        )
        summary = completion.choices[0].message.content
        logger.info("Суммаризация текста выполнена успешно.")
        return summary

    except Exception as e:
        logger.error("Ошибка при суммаризации текста: %s", e, exc_info=True)
        raise
