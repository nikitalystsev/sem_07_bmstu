import math
import random

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

    def M(self):
        """
        Математическое ожидание
        """

        return (self._a + self._b) / 2

    def D(self):
        """
        Дисперсия
        """

        return (self._b - self._a) ** 2 / 12

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


class ErlangDistribution:
    """
    Класс распределения Эрланга
    """

    def __init__(self, k: int, lamb: int | float):
        """
        Инициализация атрибутов класса
        """
        self._k = k
        self._lamb = lamb

    def F(self, x: int | float):
        """
        Метод, возвращающий значение функции распределения
        """
        if x < 0:
            return 0

        right_part = sum([pow(self._lamb * x, i) / math.factorial(i)
                         for i in range(self._k)])

        return 1 - math.exp((-1) * self._lamb * x) * right_part

    def f(self, x: int | float):
        """
        Метод, возвращающий значение функции плотности распределения
        """

        if x < 0:
            return 0

        numerator = math.exp((-1) * self._lamb * x) * \
            self._lamb * pow(self._lamb * x, self._k)

        return numerator / math.factorial(self._k)

    def M(self):
        """
        Математическое ожидание
        """

        return self._k / self._lamb

    def D(self):
        """
        Дисперсия
        """

        return self._k / (self._lamb ** 2)

    def t_i(self):
        """
        Метод возвращает момент времени t_i
        """
        _sum = 0
        for _ in range(self._k):
            _sum += (1 / self._lamb) * math.log(1 - random.random())

        return - (1 / self._k) * _sum

    def set_params(self, k: int, lamb: int | float):
        """
        Сеттер
        """
        self._k = k
        self._lamb = lamb


class PoissonDistribution:
    """
    Класс распределения Пуассона
    https://www.geeksforgeeks.org/maths/poisson-distribution/ -- формулы
    """

    def __init__(self, lamb: int | float):
        """
        Инициализация атрибутов класса
        """
        self._lamb = lamb

    def F(self, x: int):
        """
        Метод, возвращающий значение функции распределения
        """
        res = 0
        factorial = 1  # для вычисления i!

        for i in range(x + 1):
            if i > 0:
                factorial *= i
            prob = (self._lamb ** i * math.exp(-self._lamb)) / factorial
            res += prob

        return res

    def p(self, x: int):
        """
        Метод, возвращающий значение функции вероятности
        """

        factorial = 1
        for i in range(1, x + 1):
            factorial *= i

        return (self._lamb ** x * math.exp(-self._lamb)) / factorial

    def M(self):
        """
        Математическое ожидание
        """

        return self._lamb

    def D(self):
        """
        Дисперсия
        """

        return self._lamb

    def t_i(self):
        """
        Метод возвращает момент времени t_i
        """
        _exp = math.exp(-self._lamb)

        x = 0

        r_i = 1
        while r_i > _exp:
            x += 1
            r_i *= random.random()

        return x - 1

    def set_lambda(self, lamb: int | float):
        """
        Сеттер
        """
        self._lamb = lamb


class ExponentialDistribution:
    """
    Класс экспоненциального распределения
    """

    def __init__(self, lamb: int | float):
        """
        Инициализация атрибутов класса
        """
        self._lamb = lamb

    def F(self, x: int | float):
        """
        Метод, возвращающий значение функции распределения
        """

        if x < 0:
            return 0

        return 1 - math.exp(-self._lamb * x)

    def f(self, x: int | float):
        """
        Метод, возвращающий значение функции плотности
        """

        if x < 0:
            return 0

        return self._lamb * math.exp(-self._lamb * x)

    def M(self):
        """
        Математическое ожидание
        """

        return 1 / self._lamb

    def D(self):
        """
        Дисперсия
        """

        return 2 / (self._lamb ** 2)

    def t_i(self):
        """
        Метод возвращает момент времени t_i
        """

        return -(1 / self._lamb) * math.log(1 - random.random())

    def set_lambda(self, lamb: int | float):
        """
        Сеттер
        """
        self._lamb = lamb


class NormalDistribution:
    """
    Класс распределения 
    """

    def __init__(self, mu: int | float, sigma: int | float):
        """
        Инициализация атрибутов класса
        """
        self._mu = mu
        self._sigma = sigma

    def F(self, x: int | float):
        """
        Метод, возвращающий значение функции распределения
        """

        return 0.5 * (1 + math.erf((x - self._mu) / math.sqrt(2 * self._sigma ** 2)))

    def f(self, x: int | float):
        """
        Метод, возвращающий значение функции плотности
        """

        return (1 / (math.sqrt(2 * math.pi) * self._sigma)) * math.exp(-((x - self._mu) ** 2) / (2 * self._sigma ** 2))

    def M(self):
        """
        Математическое ожидание
        """

        return self._mu

    def D(self):
        """
        Дисперсия
        """

        return self._sigma ** 2

    def t_i(self):
        """
        Метод возвращает момент времени t_i
        n = 12
        """
        _sum = 0
        for _ in range(6):
            _sum += random.random()

        return self._sigma * (_sum - 6) + self._mu

    def set_params(self, mu: int | float, sigma: int | float):
        """
        Сеттер
        """
        self._mu = mu
        self._sigma = sigma
