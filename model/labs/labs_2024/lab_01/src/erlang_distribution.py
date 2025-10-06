import math as m
import os

from matplotlib import pyplot as plt

X_COUNT = 100


class ErlangDistribution:
    """
    Класс распределения Эрланга
    """

    def __init__(self, k: int, lambda_: int | float):
        """
        Инициализация атрибутов класса
        """
        self.k = k
        self.lambda_ = lambda_

    def f_distribution(self, x: int | float):
        """
        Метод, возвращающий значение функции распределения
        """
        right_part = sum([pow(self.lambda_ * x, i) / m.factorial(i) for i in range(self.k + 1)])

        return 1 - m.exp((-1) * self.lambda_ * x) * right_part

    def f_distribution_density(self, x: int | float):
        """
        Метод, возвращающий значение функции плотности распределения
        """

        numerator = m.exp((-1) * self.lambda_ * x) * self.lambda_ * pow(self.lambda_ * x, self.k)

        return numerator / m.factorial(self.k)


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

    if x_min < 0:
        print("\n\nОшибка. Неверно заданы значения интервала для распределения Эрланга!\n"
              "Требуется, чтобы x_min >= 0!")
        return

    return x_min, x_max


def get_k_and_lambda():
    print("\nВВОД ПАРАМЕТРОВ ЭРЛАНГА")
    try:
        k = int(input("Введите k: "))
        _lambda = float(input("Введите λ: "))
    except ValueError:
        print("\n\nОшибка. Неверно заданы параметры для распределения Эрланга!\n"
              "k - натуральное число;\n"
              "λ - действительное число.")
        return

    if k < 0 or _lambda < 0:
        print("\n\nОшибка. Неверно заданы параметры для распределения Эрланга!\n"
              "Требуется, чтобы λ >= 0, k = 0, 1, 2, ...!")
        return

    return k, _lambda


def draw_erlang_distribution_graphs(erlang_distribution: ErlangDistribution):
    """
    Функция для построения графика функции распределения Эрланга
    """
    x_ranges = get_interval_x_min_x_max()
    if x_ranges is None:
        return

    x_min, x_max = x_ranges

    x_list = list()
    erlang_distribution_list = list()
    erlang_distribution_density_list = list()

    k, lambda_ = erlang_distribution.k, erlang_distribution.lambda_
    step = (x_max - x_min) / X_COUNT
    x = x_min

    while x <= x_max:
        erlang_distribution_list.append(erlang_distribution.f_distribution(x))
        erlang_distribution_density_list.append(erlang_distribution.f_distribution_density(x))
        x_list.append(x)
        x += step

    plt.figure(figsize=(9, 3))

    plt.subplot(121)
    plt.plot(x_list, erlang_distribution_list)
    plt.title('Функция распределения')
    plt.xlabel('x')
    plt.ylabel(f'F_{k}(x)')
    plt.grid(True)

    plt.subplot(122)
    plt.plot(x_list, erlang_distribution_density_list)
    plt.title('Функция плотности распределения')
    plt.xlabel('x')
    plt.ylabel(f'f_{k}(x)')
    plt.grid(True)

    if not os.path.isdir(f"../data/erlang"):
        os.mkdir(f"../data/erlang")

    filename = f"../data/erlang/ed_{k}_{lambda_}.svg"
    plt.savefig(filename, format="svg")

    plt.show()
