"""Модуль движка базы данных."""
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import aiofiles

from app.utils.logger import setup_logger
from config import config


logger = setup_logger(__name__)

engine = create_async_engine(config.database_url, future=True)
Base = declarative_base()

async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def database_exists() -> bool:
    """
    Проверяет, инициализирована ли база данных, проверяя наличие таблиц.

    :return: True, если база данных инициализирована, иначе False.
    """
    async with engine.connect() as conn:
        result = await conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table';")
        )
        tables = result.fetchall()
        return len(tables) > 0


async def initialize_database(schema_path: str = 'schema.sql') -> None:
    """
    Инициализирует базу данных, выполняя файл schema.sql, если база данных
    еще не инициализирована.
    """
    try:
        os.makedirs('database', exist_ok=True)
        if not await database_exists():
            async with engine.begin() as conn:
                logger.info("Инициализация базы данных.")
                async with aiofiles.open(schema_path, mode='r') as f:
                    schema = await f.read()
                statements = schema.split(';')
                for statement in statements:
                    if statement.strip():
                        await conn.execute(text(statement))
                logger.info("База данных инициализирована успешно.")
        else:
            logger.info(
                "База данных уже инициализирована. Пропуск инициализации."
            )
    except SQLAlchemyError as e:
        logger.error(
            "Инициализация базы данных не удалась: %s", e, exc_info=True
        )
        raise
