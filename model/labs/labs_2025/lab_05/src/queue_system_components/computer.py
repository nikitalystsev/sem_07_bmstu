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

    def t_i(self):
        """
        Метод возвращает момент времени t_i
        """

        return self._a + (self._b - self._a) * random.random()

    def set_params(self, a: int | float, b: int | float) -> None:
        """
        Метод устанавливает значения параметров распределения
        """
        self._a = a
        self._b = b

    def get_a(self):
        """
        Геттер
        """
        return self._a

    def get_b(self):
        """
        Геттер
        """
        return self._b
