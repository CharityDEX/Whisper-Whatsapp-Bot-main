"""Инициализация модулей utils."""
from config import config
from .openai_creator import OpenAICreator


openai_client = OpenAICreator.create_openai_client(
    config.openai_api_key,
    config.proxy
)
