"""Установка маршрутов (Инициализация)."""
from fastapi import FastAPI, Depends
from .webhook import router as webhook_router
from app.whapi.authorization import authenticate_token


def setup_routers(app: FastAPI) -> None:
    """Установка маршрутов."""
    app.include_router(
        webhook_router,
        dependencies=[Depends(authenticate_token)]
    )
