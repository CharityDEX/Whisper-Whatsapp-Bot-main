"""Вебхук для WHAPI. (прием запросов)"""
import asyncio
from typing import Dict
from fastapi import APIRouter, Request
from app.middleware import middleware
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.post("/webhook")
async def webhook(request: Request) -> Dict[str, str]:
    """
    Получение веб хука

    :param request: Запрос
    :return: Ответ
    """
    body = await request.json()
    try:
        asyncio.create_task(middleware(body))
    except Exception as e:
        logger.error("Ошибка обработки веб хука: %s", e, exc_info=True)
        return {"message": f"error: {str(e)}"}

    return {"message": "ok"}
