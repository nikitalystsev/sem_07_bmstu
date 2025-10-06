# from tkinter import ttk
import tkinter as tk
import numpy as np
from random import randint
from tkinter import messagebox

import config_GUI as cfg
from table import Table
from prng import TabularGenerator, CriterionOfRandom, LaggedFibonacciGenerator
from checks import check_int
# from PointClass import Point


class MyWindow(tk.Tk):
    """
    Интерфейс программы
    """

    def __init__(self):
        """
        Инициализация атрибутов класса
        """
        super().__init__()

        self.cfgWin = cfg.ConfigGUI()

    
        self.title("Лабораторная №1, Лысцев Никита ИУ7-73Б")

        root_width = 1280
        root_height = 720
        self.geometry(f"{root_width}x{root_height}+0+0")
        self.resizable(width=False, height=False)
        self.config(background="#3D517F")

        self._frame_tbl_way = self.__create_frame(self)
        self._frame_tbl_way.config(background="#3D517F")
        self._frame_tbl_way.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self._frame_alg_way = self.__create_frame(self)
        self._frame_alg_way.config(background="#b0b0b0")
        self._frame_alg_way.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        self._frame_manual_way = self.__create_frame(self)
        self._frame_manual_way.config(background="#3D517F")
        self._frame_manual_way.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self._lbl_table_way = self.__create_label(
            master=self._frame_tbl_way, text="Табличный способ")
        self._lbl_table_way.config(padx=50, pady=50, background="#3D517F", font=(
            self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE))
        self._lbl_table_way.pack()

        self._lbl_alg_way = self.__create_label(
            master=self._frame_alg_way, text="Алгоритмический способ")
        self._lbl_alg_way.config(padx=50, pady=50, background="#b0b0b0", font=(
            self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE))
        self._lbl_alg_way.pack()

        self._lbl_manual_way = self.__create_label(
            master=self._frame_manual_way, text="Ручной ввод")
        self._lbl_manual_way.config(padx=50, pady=50, background="#3D517F", font=(
            self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE))
        self._lbl_manual_way.pack()

        # таблицы чисел
        self._tbl_table_way = Table(
            master=self._frame_tbl_way, cnt_rows=10, cnt_cols=3, entries_state="disabled", headers=("1", "2", "3"))
        self._tbl_table_way.pack()
        self.__fill_tbl_table()
        
        self._tbl_alg_way = Table(
            master=self._frame_alg_way, cnt_rows=10, cnt_cols=3, entries_state="disabled", headers=("1", "2", "3"))
        self._tbl_alg_way.pack()
        self.__fill_alg_table()
        
        self._tbl_manual_way = Table(
            master=self._frame_manual_way, cnt_rows=10, cnt_cols=1, entries_state="normal", headers=("1"))
        self._tbl_manual_way.pack()
        # --------------------------------------------
        
        
        self._lbl_table_way_coeff = self.__create_label(
            master=self._frame_tbl_way, text="Коэффициенты")
        self._lbl_table_way_coeff.config(padx=50, pady=50, background="#3D517F", font=(
            self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE))
        self._lbl_table_way_coeff.pack()

        self._lbl_alg_way_coeff = self.__create_label(
            master=self._frame_alg_way, text="Коэффициенты")
        self._lbl_alg_way_coeff.config(padx=50, pady=50, background="#b0b0b0", font=(
            self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE))
        self._lbl_alg_way_coeff.pack()

        self._lbl_manual_way_coeff = self.__create_label(
            master=self._frame_manual_way, text="Коэффициент")
        self._lbl_manual_way_coeff.config(padx=50, pady=50, background="#3D517F", font=(
            self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE))
        self._lbl_manual_way_coeff.pack()

        # таблицы коэффициентов
        self._tbl_table_way_coeff = Table(
            master=self._frame_tbl_way, cnt_rows=1, cnt_cols=3, entries_state="disabled", headers=("1", "2", "3"))
        self._tbl_table_way_coeff.pack(padx=50)

        self._tbl_alg_way_coeff = Table(
            master=self._frame_alg_way, cnt_rows=1, cnt_cols=3, entries_state="disabled", headers=("1", "2", "3"))
        self._tbl_alg_way_coeff.pack(padx=50)

        self._tbl_manual_way_coeff = Table(
            master=self._frame_manual_way, cnt_rows=1, cnt_cols=1, entries_state="disabled", headers=("1"))
        self._tbl_manual_way_coeff.pack(padx=50)
        # ------------------------------------
        
        self._btn_table_way_calc = self.__create_button(
            self._frame_tbl_way, text="Вычислить")
        self._btn_table_way_calc.config(background="#d9d9d9", font=(
            self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE), relief=tk.GROOVE)
        self._btn_table_way_calc.config(command=self.__calc_table_coeff)
        self._btn_table_way_calc.pack(pady=40)

        self._frame_alg_way_btns = self.__create_frame(self._frame_alg_way)
        self._frame_alg_way_btns.pack(pady=40)
        
        self._btn_alg_way_gen = self.__create_button(
            self._frame_alg_way_btns, text="Сгенерировать")
        self._btn_alg_way_gen.config(background="#d9d9d9", font=(
            self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE), relief=tk.GROOVE)
        self._btn_alg_way_gen.config(command=self.__fill_alg_table)
        self._btn_alg_way_gen.pack(side=tk.LEFT)

        self._btn_alg_way_calc = self.__create_button(
            self._frame_alg_way_btns, text="Вычислить")
        self._btn_alg_way_calc.config(background="#d9d9d9", font=(
            self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE), relief=tk.GROOVE)
        self._btn_alg_way_calc.config(command=self.__calc_alg_coeff)
        self._btn_alg_way_calc.pack(side=tk.LEFT)
        
        self._btn_manual_way_calc = self.__create_button(
            self._frame_manual_way, text="Вычислить")
        self._btn_manual_way_calc.config(background="#d9d9d9", font=(
            self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE), relief=tk.GROOVE)
        self._btn_manual_way_calc.config(command=self.__calc_manual_coeff)
        self._btn_manual_way_calc.pack(pady=40)

        # self._frame_tbl_way = self.__create_frame()
        # self._frame_tbl_way.pack(side=tk.LEFT, anchor="n", fill="both", expand=True)

        # создал фреймы для всего
        # -----------------------------------------------
        # self._frame_widgets = self.__create_frame_widgets()
        # self._frame_widgets.config(bg="#3D517F")
        # self._frame_widgets.pack(side=tk.LEFT, anchor="n", fill="both")
        # self._display = self.__create_display()
        # self._display.pack(side=tk.LEFT, expand=True, anchor="n", fill="both")
        # -----------------------------------------------

        # виджеты
        # -----------------------------------------------
        # self._var_input_cnt_states = tk.StringVar()
        # self._var_input_cnt_states.trace_add("write")

        # self._lbl_input_cnt_states = self.__create_label("Количество состояний")
        # self._lbl_input_cnt_states.config(font=(self.cfgWin.FONT, 18), relief=tk.RAISED)
        # self._lbl_input_cnt_states.grid(row=0, column=0, columnspan=4, sticky='wens', padx=10, pady=10)

        # self._entry_input_cnt_states = self.__create_entry()
        # self._entry_input_cnt_states.config(textvariable=self._var_input_cnt_states)
        # self._entry_input_cnt_states.grid(row=1, column=0, columnspan=4, sticky='wens', padx=10, pady=10)

        # self._btn_calculate = self.__create_button("Вычислить")
        # self._btn_calculate.config(font=(self.cfgWin.FONT, 18))
        # self._btn_calculate.grid(row=2, column=0, columnspan=4, sticky='wens', padx=10, pady=10)

        # self._btn_graph_states_probs = self.__create_button("Построить графики\n вероятностей состояний")
        # self._btn_graph_states_probs.config(font=(self.cfgWin.FONT, 18))
        # self._btn_graph_states_probs.grid(row=3, column=0, columnspan=4, sticky='wens', padx=10, pady=10)

        # self._lbl_empty = self.__create_label("")
        # self._lbl_empty.config(bg="#3D517F")
        # self._lbl_empty.grid(row=4, column=0, columnspan=4, sticky='wens')

        # self._btn_gen_random_intens = self.__create_button("Сгенерировать случайные\n интенсивности")
        # self._btn_gen_random_intens.config(font=(self.cfgWin.FONT, 18))
        # self._btn_gen_random_intens.grid(row=5, column=0, columnspan=4, sticky='wens', padx=10, pady=10)

    # o
    #     self._rbt_funcs = tk.StringVar(value=self._tuple_funcs[0])
    #
    #     self._btn_func0 = self.__create_radiobutton(self._tuple_funcs[0])
    #     self._btn_func0.grid(row=1, column=1, columnspan=3, sticky='wens')
    #
    #     self._btn_func1 = self.__create_radiobutton(self._tuple_funcs[1])
    #     self._btn_func1.grid(row=2, column=1, columnspan=3, sticky='wens')
    #
    #     self._btn_func2 = self.__create_radiobutton(self._tuple_funcs[2])
    #     self._btn_func2.grid(row=3, column=1, columnspan=3, sticky='wens')
    #
    #     self._btn_func3 = self.__create_radiobutton(self._tuple_funcs[3])
    #     self._btn_func3.grid(row=4, column=1, columnspan=3, sticky='wens')
    #
    #     self._btn_print_graph = self.__create_button("Отобразить график")
    #     self._btn_print_graph.config(command=self.__create_graph, font=(FONT, 16))
    #     self._btn_print_graph.grid(row=5, column=0, columnspan=4, sticky='wens')
    #
    #     # виджеты для выбора пределов и шага по осям Ox и Oz
    #     # -----------------------------------------------
    #     self._lbl_choice_limits = self.__create_label("Выбор пределов")
    #     self._lbl_choice_limits.config(font=(FONT, 18, 'bold', "underline"))
    #     self._lbl_choice_limits.grid(row=6, column=0, columnspan=4, sticky='wens')
    #
    #     self._lbl_from = self.__create_label("От: ")
    #     self._lbl_from.grid(row=7, column=1, sticky='wens')
    #
    #     self._lbl_to = self.__create_label("До: ")
    #     self._lbl_to.grid(row=7, column=2, sticky='wens')
    #
    #     self._lbl_step = self.__create_label("Шаг: ")
    #     self._lbl_step.grid(row=7, column=3, sticky='wens')
    #
    #     self._lbl_x_axis = self.__create_label("Ось X: ")
    #     self._lbl_x_axis.grid(row=8, column=0, sticky='wens')
    #
    #     self._entry_x_from = self.__create_entry()
    #     self._entry_x_from.grid(row=8, column=1, sticky='wens')
    #
    #     self._entry_x_to = self.__create_entry()
    #     self._entry_x_to.grid(row=8, column=2, sticky='wens')
    #
    #     self._entry_x_step = self.__create_entry()
    #     self._entry_x_step.grid(row=8, column=3, sticky='wens')
    #
    #     self._lbl_z_axis = self.__create_label("Ось Z: ")
    #     self._lbl_z_axis.grid(row=9, column=0, sticky='wens')
    #
    #     self._entry_z_from = self.__create_entry()
    #     self._entry_z_from.grid(row=9, column=1, sticky='wens')
    #
    #     self._entry_z_to = self.__create_entry()
    #     self._entry_z_to.grid(row=9, column=2, sticky='wens')
    #
    #     self._entry_z_step = self.__create_entry()
    #     self._entry_z_step.grid(row=9, column=3, sticky='wens')
    #
    #     # виджеты для вращения фигуры
    #     # -----------------------------------------------
    #     self._lbl_rotate = self.__create_label("Вращение поверхности")
    #     self._lbl_rotate.config(font=(FONT, 18, 'bold', "underline"))
    #     self._lbl_rotate.grid(row=10, column=0, columnspan=4, sticky='wens')
    #
    #     self._lbl_x_rotate = self.__create_label("Ось X: ")
    #     self._lbl_x_rotate.grid(row=11, column=0, sticky='wens')
    #
    #     self._entry_x_rotate = self.__create_entry()
    #     self._entry_x_rotate.grid(row=11, column=1, sticky='wens')
    #
    #     self._btn_x_rotate = self.__create_button("Повернуть")
    #     self._btn_x_rotate.config(command=self.__rotate_graph_around_x, font=(FONT, 16))
    #     self._btn_x_rotate.grid(row=11, column=2, columnspan=2, sticky='wens')
    #
    #     self._lbl_y_rotate = self.__create_label("Ось Y: ")
    #     self._lbl_y_rotate.grid(row=12, column=0, sticky='wens')
    #
    #     self._entry_y_rotate = self.__create_entry()
    #     self._entry_y_rotate.grid(row=12, column=1, sticky='wens')
    #
    #     self._btn_y_rotate = self.__create_button("Повернуть")
    #     self._btn_y_rotate.config(command=self.__rotate_graph_around_y, font=(FONT, 16))
    #     self._btn_y_rotate.grid(row=12, column=2, columnspan=2, sticky='wens')
    #
    #     self._lbl_z_rotate = self.__create_label("Ось Z: ")
    #     self._lbl_z_rotate.grid(row=13, column=0, sticky='wens')
    #
    #     self._entry_z_rotate = self.__create_entry()
    #     self._entry_z_rotate.grid(row=13, column=1, sticky='wens')
    #
    #     self._btn_z_rotate = self.__create_button("Повернуть")
    #     self._btn_z_rotate.config(command=self.__rotate_graph_around_z, font=(FONT, 16))
    #     self._btn_z_rotate.grid(row=13, column=2, columnspan=2, sticky='wens')
    #
    #     # виджеты справки
    #     # -----------------------------------------------
    #     self._btn_clean_plane = self.__create_button("Очистить экран")
    #     self._btn_clean_plane.config(command=self.__clean_plane, font=(FONT, 16))
    #     self._btn_clean_plane.grid(row=24, column=0, columnspan=4, sticky='wens')
    #
    #     self._btn_info = self.__create_button("Справка")
    #     self._btn_info.config(command=self.__print_info, font=(FONT, 16))
    #     self._btn_info.grid(row=25, column=0, columnspan=4, sticky='wens')
    #     # -----------------------------------------------
    #

    # def __create_frame_widgets(self) -> tk.Frame:
    #     """
    #     Метод создает фрейм для виджетов
    #     :return: фрейм для виджетов
    #     """

    #     frame_widgets = tk.Frame(
    #         master=self,
    #         width=self.cfgWin.FRAME_WIDGET_WIDTH,
    #         background=self.cfgWin.WHITE,
    #     )

    #     for i in range(4):
    #         frame_widgets.columnconfigure(index=i, weight=1, minsize=99)

    #     return frame_widgets

    def __create_frame(self, master) -> tk.Frame:
        """
        Метод создает фрейм
        """

        frame = tk.Frame(
            master=master,
        )

        return frame

    def __create_label(self, master: tk.Tk | tk.Frame, text: str) -> tk.Label:
        """
        Метод создает виджет текста (label)
        :param text: строка текста
        :return: виджет текста
        """
        label = tk.Label(
            master=master,
            text=text,
            font=(self.cfgWin.FONT, self.cfgWin.FONT_SIZE,
                  self.cfgWin.FONT_STYLE),  # default
            background=self.cfgWin.WHITE,
        )

        return label

    def __create_button(self, master: tk.Tk | tk.Frame, text: str) -> tk.Button:
        """
        Метод создает виджет кнопки (button)
        :param text:  текст
        :return: виджет кнопки
        """
        button = tk.Button(
            master=master,
            text=text,
            font=(self.cfgWin.FONT, self.cfgWin.FONT_SIZE,
                  self.cfgWin.FONT_STYLE),  # default
            background="#758BBF",
            relief=tk.RAISED
        )

        return button

    def __fill_tbl_table(self) -> None:
        """
        Метод заполняет таблицу табличного метода
        """
        
        result_one_digit = TabularGenerator().get_numbers(1)
        result_two_digits = TabularGenerator().get_numbers(2)
        result_three_digits = TabularGenerator().get_numbers(3)
        
        data: list[list[str]] = []
        
        for one, two, three in zip(result_one_digit, result_two_digits, result_three_digits):
            data.append(list(map(str, [one, two, three])))
        
        self._tbl_table_way.set_data(data=data)
    
    
    def __calc_table_coeff(self) -> None:
        """
        Метод считает критерий случайности табличного метода
        """
        
        data: list[list[str]] = self._tbl_table_way.get_data()

        _data: np.ndarray = np.array(data).T
        
        coeff_one_digit: float = CriterionOfRandom(list(map(int, _data[0]))).get_coeff()
        coeff_two_digits: float = CriterionOfRandom(list(map(int, _data[1]))).get_coeff()
        coeff_three_digits: float = CriterionOfRandom(list(map(int, _data[2]))).get_coeff()
        
        
        result: list[list[str]] = []
        
        tmp: list[str] = []
        for elem in [coeff_one_digit, coeff_two_digits, coeff_three_digits]:
            tmp.append(f"{int(elem * 100)}%")
            # tmp.append(f"{elem: .6f}")
        
        result.append(tmp)
        
        self._tbl_table_way_coeff.set_data(data=result)
        
    def __fill_alg_table(self) -> None:
        """
        Метод заполняет таблицу алгоритмического метода
        """
        seed: list[int] = [randint(0, 2**32 - 1) for _ in range(55)]
        gen = LaggedFibonacciGenerator(seed)

        # random_num = gen.next()
        result: list[list[int]] = []
        
        tmp: list[int] = []
        for _ in range(10):
            tmp.append(gen.randrange(0, 9))
        result.append(tmp)
        
        tmp: list[int] = []
        for _ in range(10):
            tmp.append(gen.randrange(10, 99))
        result.append(tmp)
        
        tmp: list[int] = []
        for _ in range(10):
            tmp.append(gen.randrange(100, 999))
        result.append(tmp)
        
        # print(f"[+] result: {result}")
        
        _result = list(np.array(result).T)
        
        # print("[+] _result: {_result}")
        
        self._tbl_alg_way.set_data(data=_result)
        
    def __calc_alg_coeff(self) -> None:
        """
        Метод считает критерий случайности алгоритмического метода
        """
        
        # print("__calc_alg_coeff is called")
        
        data: list[list[str]] = self._tbl_alg_way.get_data()

        _data: np.ndarray = np.array(data).T
        
        coeff_one_digit: float = CriterionOfRandom(list(map(int, _data[0]))).get_coeff()
        coeff_two_digits: float = CriterionOfRandom(list(map(int, _data[1]))).get_coeff()
        coeff_three_digits: float = CriterionOfRandom(list(map(int, _data[2]))).get_coeff()
        
        result: list[list[str]] = []
        
        tmp: list[str] = []
        for elem in [coeff_one_digit, coeff_two_digits, coeff_three_digits]:
            tmp.append(f"{int(elem * 100)}%")
        
        result.append(tmp)
        
        self._tbl_alg_way_coeff.set_data(data=result)
        
    def __calc_manual_coeff(self) -> None:
        """
        Метод считает критерий случайности ручного ввода
        """
        
        data = self._tbl_manual_way.get_data()

        if not self.__check_input(data):
            messagebox.showwarning("Ошибка ввода!", "Необходимо вводить цифры от 0 до 9")
            return
        
        _data: np.ndarray = np.array(data).T
        
        coeff_one_digit: float = CriterionOfRandom(list(map(int, _data[0]))).get_coeff()
        
        result: list[list[str]] = []
        
        tmp: list[str] = []
        for elem in [coeff_one_digit]:
            tmp.append(f"{int(elem * 100)}%")
            # tmp.append(f"{elem: .6f}")
        
        result.append(tmp)
        
        self._tbl_manual_way_coeff.set_data(data=result)
        
    def __check_input(self, data) -> bool:
        """
        Проверка данных
        """
        for i in range(len(data)):
            for j in range(len(data[0])):
                elem = data[i][j]
                if not check_int(elem):
                    return False
                elem = int(elem)
                if elem > 9 or elem < 0:
                    return False
                
        return True
    # def __create_entry(self) -> tk.Entry:
    #     """
    #     Метод создает виджет однострочного поля ввода (entry)
    #     :return: виджет однострочного поля ввода
    #     """
    #     entry = tk.Entry(
    #         self._frame_widgets,
    #         width=self.cfgWin.ENTRY_WIDTH,  # default
    #         relief=tk.SUNKEN,
    #         borderwidth=self.cfgWin.ENTRY_BORDER_WIDTH,  # default
    #         justify=tk.CENTER,
    #         font=(self.cfgWin.FONT, self.cfgWin.FONT_SIZE, self.cfgWin.FONT_STYLE),  # default
    #     )

    #     return entry

    # def __create_radiobutton(self, text: str) -> tk.Radiobutton:
    #     """
    #     Метод создает переключатель 2-х множеств треугольника для ввода
    #     :param text: значение переключателя
    #     :return: переключатель 2-х множеств треугольника для ввода
    #     """
    #     rbt = tk.Radiobutton(
    #         self._frame_widgets,
    #         text=text,
    #         value=text,
    #         variable=self._rbt_funcs,
    #         font=(FONT, 16, 'bold'),
    #         anchor=tk.W
    #     )
    #
    #     return rbt
    #
