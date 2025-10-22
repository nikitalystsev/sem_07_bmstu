import os

import matplotlib.pyplot as plt

X_COUNT = 100


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

    def F(self, x: int | float):
        """
        Метод, возвращающий значение функции распределения
        """
        if x < self.a:
            return 0

        if x > self.b:
            return 1

        return (x - self.a) / (self.b - self.a)

    def f(self, x: int | float):
        """
        Метод, возвращающий значение функции плотности распределения
        """
        if self.a <= x <= self.b:
            return 1 / (self.b - self.a)

        return 0


def get_interval_x_min_x_max():
    print("\nВВОД ИНТЕРВАЛОВ ВЫВОДА")
    try:
        x_min = float(input("Введите x_min: "))
        x_max = float(input("Введите x_max: "))
    except ValueError:
        print("\n\nОшибка ввода значений интервалов!")
        return

    if x_min >= x_max:
        print("\n\nНеверно заданы значения интервала. Требуется, чтобы x_min < x_max!")
        return

    return x_min, x_max


def get_interval_a_b():
    print("\nВВОД ПАРАМЕТРОВ РАВНОМЕРНОГО")
    try:
        a = float(input("Введите a: "))
        b = float(input("Введите b: "))
    except ValueError:
        print("\n\nОшибка ввода значений интервалов!")
        return

    if a >= b:
        print("\n\nНеверно заданы значения интервала. Требуется, чтобы a < b!")
        return

    return a, b


def draw_uniform_distribution_graphs(
        uniform_distribution: UniformDistribution,
):
    """
    Функция для построения графика функции равномерного распределения
    """
    x_ranges = get_interval_x_min_x_max()
    if x_ranges is None:
        return

    x_min, x_max = x_ranges

    x_list = list()
    uniform_distribution_list = list()
    uniform_distribution_density_list = list()

    a, b = uniform_distribution.a, uniform_distribution.b
    step = (x_max - x_min) / X_COUNT
    x = x_min

    while x <= x_max:
        uniform_distribution_list.append(uniform_distribution.F(x))
        uniform_distribution_density_list.append(uniform_distribution.f(x))
        x_list.append(x)
        x += step

    plt.figure(figsize=(9, 3))

    plt.subplot(121)
    plt.plot(x_list, uniform_distribution_list)
    plt.title('Функция распределения')
    plt.xlabel('x')
    plt.ylabel('F(x)')
    plt.grid(True)

    plt.subplot(122)
    plt.plot(x_list, uniform_distribution_density_list)
    plt.title('Функция плотности распределения')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)

    if not os.path.isdir(f"../data/uniform"):
        os.mkdir(f"../data/uniform")

    filename = f"../data/uniform/ud_{a}_{b}.svg"
    plt.savefig(filename, format="svg")

    plt.show()
