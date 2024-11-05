"""
Модуль для управления пользователями, которые находятся в процессе обработки
"""


class InProcessList:
    """Класс для управления номерами пользователей, которые находятся в 
    процессе обработки."""

    def __init__(self) -> None:
        self.user_numbers = set()

    def add_user(self, number: str) -> None:
        """
        Добавить номер пользователя в таблицу.

        :param number: Номер пользователя
        """
        self.user_numbers.add(number)

    def remove_user(self, number: str) -> None:
        """
        Удалить номер пользователя из таблицы.

        :param number: Номер пользователя
        """
        if number in self.user_numbers:
            self.user_numbers.discard(number)

    def user_exists(self, number: str) -> bool:
        """
        Проверить, находится ли номер пользователя в таблице.

        :param number: Номер пользователя
        """
        return number in self.user_numbers
