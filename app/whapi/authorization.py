"""Модуль авторизации WHAPI (для защиты от неавторизованного доступа)."""
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.utils.logger import setup_logger
from app.whapi import whapi_client
from typing import Annotated

logger = setup_logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_token(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> None:
    """
    Аутентификация токена

    :param token: Токен
    :raises HTTPException: Если токен недействителен.
    """
    if token != whapi_client.authorization_token:
        logger.warning("Неавторизованный доступ с токеном: %s", token)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
