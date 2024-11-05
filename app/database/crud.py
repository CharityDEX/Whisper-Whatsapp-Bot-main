"""Операции CRUD."""
from typing import AsyncGenerator, Type, TypeVar
from contextlib import asynccontextmanager
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.utils.logger import setup_logger
from .engine import async_session_factory

T = TypeVar('T')

logger = setup_logger(__name__)


class CRUD:
    """Общий класс для обработки операций CRUD для любой модели."""

    def __init__(
        self,
        model: Type[T],
        session_factory: sessionmaker = async_session_factory
    ) -> None:
        """
        Инициализация класса CRUD.

        :param model: Модель для обработки.
        :param session_factory: Фабрика сессий для использования.
        """
        self.model = model
        self.session_factory = session_factory

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Получить асинхронную сессию."""
        session = self.session_factory()
        try:
            yield session
        finally:
            await session.close()

    async def create(self, **kwargs) -> T:
        """Создать новую запись в базе данных."""
        async with self.get_session() as session:
            instance = self.model(**kwargs)
            session.add(instance)
            try:
                await session.commit()
                await session.refresh(instance)
                logger.info(
                    "%s создан по номеру: %s",
                    self.model.__name__,
                    getattr(instance, 'number', 'unknown')
                )
                return instance
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(
                    "Не удалось создать %s: %s",
                    self.model.__name__,
                    e
                )
                raise

    async def get(self, number: int) -> T:
        """Получить запись по ID."""
        async with self.get_session() as session:
            instance = await session.get(self.model, number)
            if instance:
                logger.info(
                    "%s получен по номеру: %s",
                    self.model.__name__,
                    number
                )
            else:
                logger.warning(
                    "%s с номером %s не найден.",
                    self.model.__name__,
                    number
                )
            return instance

    async def update(self, instance: T, **kwargs) -> T:
        """Обновить информацию о записи."""
        async with self.get_session() as session:
            instance = await session.merge(instance)
            for key, value in kwargs.items():
                setattr(instance, key, value)
            try:
                await session.commit()
                await session.refresh(instance)
                logger.info(
                    "%s обновлен по номеру: %s",
                    self.model.__name__,
                    getattr(instance, 'number', 'unknown')
                )
                return instance
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(
                    "Не удалось обновить %s: %s",
                    self.model.__name__,
                    e
                )
                raise

    async def delete(self, instance: T) -> bool:
        """Удалить запись."""
        async with self.get_session() as session:
            instance = await session.merge(instance)
            try:
                await session.delete(instance)
                await session.commit()
                logger.info(
                    "%s удален по номеру: %s",
                    self.model.__name__,
                    getattr(instance, 'number', 'unknown')
                )
                return True
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(
                    "Не удалось удалить %s: %s",
                    self.model.__name__,
                    e
                )
                raise
