import numpy as np


class KolmogorovEqSolver:
    """
    Класс для нахождения предельных вероятностей
    путем решения системы уравнений Колмогорова
    https://present5.com/1-3-markovskie-processy-1-opredelenie-i/ -- общий вид системы уравнений Колмогорова
    """

    def __init__(self, mtr_intens: list[list[int | float]] | np.ndarray) -> None:
        """
        Инициализация атрибутов класса
        """
        self.__mtr_intens = mtr_intens
        self.__mtr_coeff = self.__get_mtr_coeff()
        self.__list_right_part = self.__get_right_part()

        # print(f"mtr_coeff size: {len(self.__mtr_coeff)}x{len(self.__mtr_coeff[0])}")
        # print(f"right_part size: {len(self.__list_right_part)}")

    def __get_row_mtr_coeff(self, row_ind: int) -> list[float]:
        """
        Метод для получения строки матрицы коэффициентов (убираю дубликаты кода)
        """
        tmp = list()

        for j in range(len(self.__mtr_intens[0])):
            if row_ind == j:
                res = -sum(self.__mtr_intens[row_ind][:j]) - sum(self.__mtr_intens[row_ind][j + 1:])
                tmp.append(res)
            else:
                tmp.append(self.__mtr_intens[j][row_ind])

        return tmp

    def __get_mtr_coeff(self) -> list[list[int | float]]:
        """
        Метод для получения матрицы коэффициентов
        системы уравнений Колмогорова
        """
        mtr_coeff: list[list[int | float]] = list()

        # сами уравнения (без последнего, т. к. любое из уравнений является ЛК других)
        for i in range(len(self.__mtr_intens) - 1):
            mtr_coeff.append(self.__get_row_mtr_coeff(i))

        # условие нормировки
        mtr_coeff = self.__add_normalisation_cond(mtr_coeff)

        return mtr_coeff

    def get_mtr_coeff_for_graphs(self) -> list[list[int | float]]:
        """
        Метод для получения матрицы коэффициентов
        системы уравнений Колмогорова для графиков (без условия нормировки)
        """
        mtr_coeff: list[list[int | float]] = list()

        # сами уравнения (без последнего, т. к. любое из уравнений является ЛК других)
        for i in range(len(self.__mtr_intens)):
            mtr_coeff.append(self.__get_row_mtr_coeff(i))

        return mtr_coeff

    @staticmethod
    def __add_normalisation_cond(mtr_coeff: list[list[int | float]]) -> list[list[int | float]]:
        """
        Метод добавляет к исходной системе уравнений Колмогорова
        строку с условием нормировки
        """
        mtr_coeff.append([1 for _ in range(len(mtr_coeff[0]))])

        return mtr_coeff

    def __get_right_part(self) -> list[int | float]:
        """
        Метод для получения правой части системы уравнений Колмогорова
        """

        return [0 for _ in range(len(self.__mtr_intens) - 1)] + [1]

    @staticmethod
    def solve_ode(y0, _, mtr_coeff):
        """
        Вызываемая функция для решения системы дифференциальных уравнений
        """
        dydt = list()

        for i in range(len(y0)):
            res = sum(y0[j] * mtr_coeff[i][j] for j in range(len(y0)))
            dydt.append(res)

        return dydt

    def solve(self):
        """
        Метод решает систему
        """
        mtr_coeff = np.array(self.__mtr_coeff)
        list_right_part = np.array(self.__list_right_part)

        probs = np.linalg.solve(mtr_coeff, list_right_part)

        mtr_intens = np.array(self.__mtr_intens)

        v = mtr_intens.sum(axis=0) - mtr_intens.diagonal()

        stable_times = probs / v

        # print(stable_times, probs, v, mtr_intens, mtr_intens.sum(axis=1), mtr_intens.diagonal(), sep='\n\n')

        return probs, stable_times
