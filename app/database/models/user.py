"""Модель пользователя базы данных."""
from sqlalchemy import (
    Column,
    BigInteger,
    DateTime,
    func,
    Integer,
    Text,
    Boolean
)
from ..engine import Base


class User(Base):
    """Модель пользователя."""

    __tablename__ = 'users'

    number = Column(BigInteger, primary_key=True)
    name = Column(Text, default=None)
    uploaded_audios = Column(Integer, default=0)
    gpt_requests = Column(Integer, default=0)
    last_summary_text = Column(Text, default=None)
    last_transcription_text = Column(Text, default=None)
    state = Column(Text, default=None)
    is_admin = Column(Boolean, default=False)
    subscription_status = Column(Text, default="free")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    def to_dict(self) -> dict:
        """Преобразовать пользователя в словарь."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
