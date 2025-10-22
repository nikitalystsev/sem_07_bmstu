

X_COUNT = 100


class UniformDistribution:
    """
    Класс равномерного распределения
    """

    def __init__(self, a: int | float, b: int | float):
        """
        Инициализация атрибутов класса
        """
        self._a = a
        self._b = b

    def F(self, x: int | float):
        """
        Метод, возвращающий значение функции распределения
        """
        if x < self._a:
            return 0

        if x > self._b:
            return 1

        return (x - self._a) / (self._b - self._a)

    def f(self, x: int | float):
        """
        Метод, возвращающий значение функции плотности распределения
        """
        if self._a <= x <= self._b:
            return 1 / (self._b - self._a)

        return 0

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
        return self._a