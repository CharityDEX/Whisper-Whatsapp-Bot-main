"""Модуль для работы с кнопками WHAPI."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Button:
    """Класс для работы с кнопками."""
    title: str
    id: str
    type: str = field(default='quick_reply')
    copy_code: Optional[str] = None
    phone_number: Optional[str] = None
    url: Optional[str] = None
    merchant_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование кнопки в словарь."""
        return {
            "type": self.type,
            "title": self.title,
            "id": self.id
        }


@dataclass
class Markup:
    """Класс для работы с разметкой."""
    buttons: List[Button]

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование разметки в словарь."""
        return {"buttons": [button.to_dict() for button in self.buttons]}
