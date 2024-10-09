import math as m


class ErlangDistribution:
    """
    Класс распределения Эрланга
    """

    def __init__(self, k: int, _lambda: int | float):
        """
        Инициализация атрибутов класса
        """
        self.k = k
        self._lambda = _lambda

    def f_distribution(self, x: int | float):
        """
        Метод, возвращающий значение функции распределения
        """
        right_part = sum([pow(self._lambda * x, i) / m.factorial(i) for i in range(self.k)])

        return 1 - m.exp((-1) * self._lambda * x) * right_part

    def f_distribution_density(self, x: int | float):
        """
        Метод, возвращающий значение функции плотности распределения
        """

        numerator = m.exp((-1) * self._lambda * x) * self._lambda * pow(self._lambda * x, self.k - 1)

        return numerator / m.factorial(self.k - 1)
