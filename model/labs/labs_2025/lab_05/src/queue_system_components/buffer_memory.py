class BufferMemory:
    """
    Класс, реализующий компонент буферной памяти СМО (она же очередь, она же накопитель)
    Cудя по условию лабы, тут объемы очередей/накопителей/буферной памяти бесконечные
    """

    def __init__(self):
        """
        Инициализация атрибутов класса
        """
        self._p: list = list()  # одномерный массив

        self._cur_len = 0

    def write_request(self, x: int | float):
        """
        Метод для вставки данных в буферную память.
        x --- какие то данные
        """
        self._p.append(x)

        self._cur_len += 1

    def read_request(self) -> tuple[bool, int | float]:
        """
        Метод для чтения данных из буферной памяти
        """
        if not self.is_empty():
            self._cur_len -= 1
            return False, self._p.pop(0)

        return True, 0

    def is_empty(self) -> bool:
        """
        Нет ли сообщений в буферной памяти?
        """

        return self._cur_len == 0

# class BufferMemory:
#     """
#     Класс, реализующий компонент буферной памяти СМО (она же очередь, она же накопитель)
#     """

#     def __init__(self):
#         """
#         Инициализация атрибутов класса
#         """
#         self._lm = 10
#         self._p: list = [0 for _ in range(self._lm)]

#         self._np = 0  # число сообщений в памяти
#         self._poln = False  # признак переполнения памяти
#         self._pust = False  # признак отсутствия сообщений
#         # номер последнего сообщения, поступившего в память (так как индексы с 0)
#         self._npos = -1
#         self._nper = -1

#     def insert_request(self, x: int | float) -> bool:
#         """
#         Метод для вставки данных в буферную память.
#         x --- какие то данные, я думаю в этой лабе это будет время генерации события
#         """
#         if self._np == self._lm:  # если буфферная память полная
#             self._poln = True
#         else:
#             self._poln = False
#             self._np += 1
#             self._npos += 1
#             self._p[self._npos] = x

#             if self._npos != self._lm - 1:  # так как индексы с 0
#                 pass
#             else:
#                 self._npos = -1

#         if self._poln:
#             return self._poln

#         return False

#     def read_request(self):
#         """
#         Метод для чтения данных из буферной памяти
#         """
#         x: float = 0
#         if self._np == 0:
#             self._pust = True
#         else:
#             self._pust = False
#             self._np -= 1
#             self._nper += 1
#             x = self._p[self._nper]

#             if self._nper != self._lm - 1:  # так как индексы с 0
#                 pass
#             else:
#                 self._nper = -1

#         if self._pust:
#             return self._pust, x

#         return False, x
