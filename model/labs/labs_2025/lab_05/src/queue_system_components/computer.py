import random


class Computer:
    """
    Класс реализющий компьютер
    """

    def __init__(self, t: int | float) -> None:
        """
        Инициализация атрибутов класса
        Если компьютер обрабатывает запрос за 30 минут, то t = 30
        """
        self._t = t

        self._is_free = True

    def t_i(self):
        """
        Метод возвращает момент времени t_i
        """

        return self._t

    def set_state(self, state: str):
        """
        Установка состояния ОА
        """
        # print(f"computer.set_state() is called, state that is gonna set = {state}")
        
        if state == "free":
            self._is_free = True
        else:
            self._is_free = False

    def is_free(self) -> bool:
        """
        Возвращает состояние ОА
        """
        return self._is_free
