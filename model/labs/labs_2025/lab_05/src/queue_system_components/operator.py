import random


class Operator:
    """
    Класс реализющий оператора
    """

    def __init__(self, a: int | float, b: int | float) -> None:
        """
        Инициализация атрибутов класса
        Если оператор обслуживает заявку в среднем за 10 +- 5 минут, то это равномерное распределение R[5,15]
        """
        self._a = a
        self._b = b

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
