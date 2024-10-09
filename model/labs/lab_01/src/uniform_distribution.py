class UniformDistribution:
    """
    Класс равномерного распределения
    """

    def __init__(self, a: int | float, b: int | float):
        """
        Инициализация атрибутов класса
        """
        self.a = a
        self.b = b

    def f_distribution(self, x: int | float):
        """
        Метод, возвращающий значение функции распределения
        """
        if x < self.a:
            return 0

        if x > self.b:
            return 1

        return (x - self.a) / (self.b - self.a)

    def f_distribution_density(self, x: int | float):
        """
        Метод, возвращающий значение функции плотности распределения
        """
        if self.a <= x <= self.b:
            return 1 / (self.b - self.a)

        return 0
