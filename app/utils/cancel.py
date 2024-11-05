"""Модуль для работы с отменами пользователя."""
from typing import Optional
from app.database.models.user import User
from app.database.crud import CRUD


async def is_user_canceled(user: User) -> bool:
    """
    Проверяет, отменил ли пользователь текущую операцию.

    :param user: Объект пользователя.
    :return: True, если пользователь отменил текущую операцию, False в 
    противном случае.
    """
    if not user:
        raise ValueError("Переданный объект пользователя не может быть None")

    if not hasattr(user, 'number'):
        raise ValueError(
            "Переданный объект пользователя не содержит атрибута 'number'"
        )

    crud = CRUD(User)
    try:
        user_data: Optional[User] = await crud.get(user.number)
        if not user_data:
            return False
        return user_data.state is None
    except Exception as e:
        raise RuntimeError(
            f"Ошибка при проверке состояния отмены пользователя: {str(e)}"
        ) from e
