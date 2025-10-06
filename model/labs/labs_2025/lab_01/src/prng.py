import random as rd
import math


DATA_FILE_PATH = "/home/nikitalystsev/Documents/bmstu/sem_07_bmstu/model/labs/labs_2025/lab_01/data/million_random_digits.txt"


class TabularGenerator:
    """
    Генерация псевдослучайных чисел из таблицы
    """

    def __init__(self, filepath: str = DATA_FILE_PATH) -> None:
        self.__filepath = filepath
        self.__unselected_row = rd.randint(0, 19999)
        self.__unselected_col = rd.randint(0, 9)

        data: tuple[int, int] = self.__get_starting_line_col()

        self.__starting_row = data[0]
        self.__starting_col = data[1]

    def get_numbers(self, digit_lenght: int, amount: int = 10) -> list[int]:
        # Считываем все строки и соберём строку цифр на каждую строку файла
        rows_digits: list[str] = []
        with open(self.__filepath, encoding="utf-8") as f:
            for row in f:
                # пропускаем первый "счётчик" столбец и склеиваем остальные числа в одну «линию» цифр
                row_digits = ''.join(row.strip().split()[1:])
                rows_digits.append(row_digits)

        if not rows_digits:
            return []

        n_rows = len(rows_digits)
        r = self.__starting_row % n_rows
        start_col = self.__starting_col

        result: list[int] = []

        while len(result) < amount:
            line = rows_digits[r]

            # если стартовая колонка слишком большая для этой строки — идём на следующую
            if start_col + digit_lenght > len(line):
                r = (r + 1) % n_rows
                continue

            pos = start_col

            # пытаемся найти окно длиной digit_lenght без ведущего нуля
            while pos + digit_lenght <= len(line):
                chunk = line[pos:pos + digit_lenght]
                if chunk[0] != '0':                 # без ведущих нулей
                    result.append(int(chunk))
                    break
                pos += 1                            # ведущий ноль? сдвигаем окно вправо и пробуем снова

            # после попытки (успешной или нет) переходим к следующей строке
            r = (r + 1) % n_rows

        return result

    def __get_starting_line_col(self):
        """
        Метод читает числа из файла
        """
        starting_line: int = 0
        starting_col: int = 0

        with open(file=self.__filepath) as file:
            for i, row in enumerate(file):
                parts: list[str] = row.strip().split()[1:]
                if i == self.__unselected_row:
                    unselected_num = parts[self.__unselected_col]

                    starting_line = self.__get_starting_line(unselected_num)
                    starting_col = self.__get_starting_col(unselected_num)

        return starting_line, starting_col

    def __get_starting_line(self, unselected_num: str) -> int:
        """
        Метод позволяет получить начальную строку
        """
        first_digit = int(unselected_num[0])

        rest = unselected_num[1:]
        mod = first_digit % 2

        result_str = str(mod) + rest

        return int(result_str)

    def __get_starting_col(self, unselected_num: str) -> int:
        """
        Метод позволяет получить начальный столбец
        """

        last_two = int(unselected_num[-2:])

        return last_two % 50


class LaggedFibonacciGenerator:
    """
    Генератор псевдослучайных чисел методом Фибоначчи с запаздыванием
    """

    def __init__(self, seed: list[int], a=24, b=55, m=2**32):
        """
        Инициализация атрибутов класса
        """
        assert len(seed) >= b, "Seed must have at least b elements"
        self.__buffer = seed[:]
        self.__a = a
        self.__b = b
        self.__m = m
        self.__index = max(a, b)

    def next(self):
        """
        Метод генерирует псевдослучайное число
        """
        # Индексы для xₙ₋a и xₙ₋b
        i = (self.__index - self.__a) % len(self.__buffer)
        j = (self.__index - self.__b) % len(self.__buffer)

        # print(f"i = {i}, j = {j}")
        
        # Генерация нового числа
        new_val = (self.__buffer[i] + self.__buffer[j]) % self.__m

        # Сохраняем в буфер и продвигаем
        self.__buffer[self.__index % len(self.__buffer)] = new_val
        # print(f"buffer index: {self.__index % len(self.__buffer)}")
        self.__index += 1

        return new_val

    def randrange(self, min_value: int, max_value: int) -> int:
        """
        Возвращает псевдослучайное число в диапазоне [min_value, max_value]
        """
        if min_value > max_value:
            raise ValueError("min_value must be <= max_value")

        range_size = max_value - min_value + 1

        return self.next() % range_size + min_value


class CriterionOfRandom:
    """
    Критерий случайности
    """

    def __init__(self, numbers: list[int]) -> None:
        self.__numbers = numbers

    def get_coeff(self) -> float:
        
        return min(self.__get_coeff_avg(), self.__get_coeff_pair())
    
    def __get_coeff_pair(self) -> float:
        """
        Проверяет случайность последовательности по критерию парного баланса.
        Считает отношение числа пар с ростом к числу пар с падением.
        Если отношение близко к 1, последовательность выглядит случайной.
        """
        cnt_pair_up = 0  
        cnt_pair_down = 0  

        for i in range(len(self.__numbers) - 1):
            if self.__numbers[i] < self.__numbers[i + 1]:
                cnt_pair_up += 1
            elif self.__numbers[i] > self.__numbers[i + 1]:
                cnt_pair_down += 1

        if cnt_pair_up == 0 or cnt_pair_down == 0:
            return 0

        coeff = cnt_pair_up / cnt_pair_down if cnt_pair_up <= cnt_pair_down else cnt_pair_down / cnt_pair_up

        print(f"Количество пар с ростом: {cnt_pair_up}")
        print(f"Количество пар с падением: {cnt_pair_down}")
        print(f"Отношение (меньшее/большее): {coeff:.6f}")

        return coeff
    
    def __get_coeff_avg(self) -> float:
        """
        Получаем коэффициент: отношение средних арифметических четных и нечетных числел
        """
        even_numbers, odd_numbers = list(), list()
        
        for num in self.__numbers:
            if num % 2 == 0:
                even_numbers.append(num)
            else:
                odd_numbers.append(num)
        
        if len(even_numbers) == 0 or len(odd_numbers) == 0:
            return 0
        
        avg_even_numbers = sum(even_numbers) / len(even_numbers)
        avg_odd_numbers = sum(odd_numbers) / len(odd_numbers)
        
        coeff = avg_odd_numbers / avg_even_numbers if avg_odd_numbers <= avg_even_numbers else avg_even_numbers / avg_odd_numbers
        
        return coeff
    
    # def get_coeff(self, bit_width=None) -> float:
    #     """
    #     Метод обертка
    #     """
    #     bits = self.__ints_to_bits(bit_width=bit_width)

    #     print(f"result: {bits}")

    #     def X_i(xi):
    #         return 2 * xi - 1

    #     S = 0

    #     for bit in bits:
    #         S += X_i(bit)

    #     S_obs = abs(S) / math.sqrt(len(bits))

    #     P_value = math.erfc(S_obs / math.sqrt(2.0))

    #     print(f"P_value = {P_value}, success = {P_value >= 0.01}")

    #     return P_value

    # def get_coeff(self, bit_width=None) -> float:
    #     """
    #     Метод обертка
    #     """
    #     bits = self.__ints_to_bits(bit_width=bit_width)

    #     print(f"result: {bits}")

    #     pi = 0
    #     for bit in bits:
    #         pi += bit if bit else 0

    #     pi = pi / len(bits)
        
    #     cond = abs(pi - 1/2) < 2/math.sqrt(len(bits))

    #     print(f"cond = {cond}")

    #     if not cond:
    #         return 0

    #     V_n = 0
    #     for i in range(0, len(bits) - 1):
    #         if bits[i] == bits[i + 1]:
    #             V_n += 0
    #         else:
    #             V_n += 1

    #     P_value = math.erfc(abs(V_n - 2 * len(bits) * pi * (1 - pi)) /
    #                         (2 * math.sqrt(2 * len(bits)) * pi * (1 - pi)))

    #     print(f"P_value = {P_value}, success = {P_value >= 0.01}")
        
    #     return P_value