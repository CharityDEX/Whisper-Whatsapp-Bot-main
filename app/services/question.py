"""Утилиты для ответа на вопросы."""
from app.utils import openai_client
from prompts import QUESTION_PROMPT
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


async def get_answer(context: str, question: str) -> str:
    """
    Получить ответ на вопрос.

    :param context: Контекст
    :param question: Вопрос
    :return: Ответ
    """
    try:
        prompt = QUESTION_PROMPT.format(context=context, question=question)
        response = await openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        logger.error(
            f"Ошибка при получении ответа на вопрос: {str(e)}", exc_info=True)
        raise
