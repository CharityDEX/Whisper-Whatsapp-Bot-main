"""Модуль для работы с данными пользователя WHAPI."""
from dataclasses import dataclass


@dataclass
class User:
    """Класс для работы с данными пользователя."""
    number: str
    chat_id: str
    source: str
    from_name: str
