"""Основной файл приложения."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import setup_routers
from app.database.engine import initialize_database
from app.utils.url_manager import URLManager
from app.whapi import whapi_client
from config import config


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Инициализация приложения

    :param app: FastAPI приложение
    """
    await initialize_database()
    url_manager = await URLManager.create(config.webhook_host)
    await whapi_client.set_webhook(
        webhook_url=url_manager.get_webhook_url()
    )
    yield

# Создание FastAPI приложения
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Установка маршрутов
setup_routers(app)
