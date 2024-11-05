"""Инициализация WHAPI модуля."""
from .api import WHAPI
from config import config

whapi_client = WHAPI(config.whapi_token)
