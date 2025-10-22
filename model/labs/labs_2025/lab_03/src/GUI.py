# from tkinter import ttk
import random
from tkinter import messagebox
import tkinter as tk
import numpy as np
import scipy.integrate as integrate
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from torch.linalg import solve

import config_GUI as cfg
from table import Table

import checks
from distribution_params_frame import DistributionParamsFrame

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

        self.title("Лабораторная №2, Лысцев Никита ИУ7-73Б")

        root_width = 1280
        root_height = 720
        self.geometry(f"{root_width}x{root_height}+0+0")
        self.resizable(width=False, height=False)

        # создал фреймы для всего
        # -----------------------------------------------
        self._frame_widgets = self.__create_frame(master=self)
        self._frame_widgets.config(bg="#3D517F")
        self._frame_widgets.columnconfigure(1, weight=1)
        self._frame_widgets.pack(side=tk.LEFT, fill="both")

        self._frame_distribution_params = DistributionParamsFrame(
            self._frame_widgets)
        self._frame_distribution_params.config(background="#3D517F")
        self._frame_distribution_params.grid(
            row=100, column=0, columnspan=4, sticky='wens')

        self._frame_results = self.__create_frame(master=self)
        self._frame_results.config(background="#b0b0b0")
        self._frame_results.pack(side=tk.LEFT, expand=True, fill="both")
        # -----------------------------------------------

        # constants
        self._uniform_distribution = "Равномерное распределение"
        self._erlang_distribution = "Распределение Эрланга"
        self._poisson_distribution = "Распределение Пуассона"
        self._exponential_distribution = "Экспоненциальное распределение"
        self._normal_distribution = "Нормальное распределение"
        # -----------------------------------------------

        # виджеты
        # -----------------------------------------------

        self._var_choice_distribution_type = tk.StringVar(
            value=self._uniform_distribution
        )

        self._lbl_input_cnt_states = self.__create_label(
            master=self._frame_widgets, text="Законы распределения")
        self._lbl_input_cnt_states.config(
            font=(self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE), background="#3D517F")
        self._lbl_input_cnt_states.grid(
            row=0, column=0, columnspan=4, sticky='wens', padx=10, pady=30)

        self._rdb_uniform_distribution = self.__create_radiobutton(
            text=self._uniform_distribution, var=self._var_choice_distribution_type
        )
        self._rdb_uniform_distribution.config(
            command=self.__pack_uniform_params
        )
        self._rdb_uniform_distribution.grid(
            row=1, column=0, columnspan=4, sticky='wens', padx=10
        )

        self._rdb_erlang_distributions = self.__create_radiobutton(
            text=self._erlang_distribution, var=self._var_choice_distribution_type
        )
        self._rdb_erlang_distributions.config(
            command=self.__pack_erlang_params
        )
        self._rdb_erlang_distributions.grid(
            row=2, column=0, columnspan=4, sticky='wens', padx=10, pady=5
        )

        self._rdb_poisson_distributions = self.__create_radiobutton(
            text=self._poisson_distribution, var=self._var_choice_distribution_type
        )
        self._rdb_poisson_distributions.config(
            command=self.__pack_poisson_params
        )
        self._rdb_poisson_distributions.grid(
            row=3, column=0, columnspan=4, sticky='wens', padx=10,
        )

        self._rdb_exponential_distributions = self.__create_radiobutton(
            text=self._exponential_distribution, var=self._var_choice_distribution_type
        )
        self._rdb_exponential_distributions.config(
            command=self.__pack_exponential_params
        )
        self._rdb_exponential_distributions.grid(
            row=4, column=0, columnspan=4, sticky='wens', padx=10, pady=5
        )

        self._rdb_normal_distributions = self.__create_radiobutton(
            text=self._normal_distribution, var=self._var_choice_distribution_type
        )
        self._rdb_normal_distributions.config(
            command=self.__pack_normal_params)
        self._rdb_normal_distributions.grid(
            row=5, column=0, columnspan=4, sticky='wens', padx=10
        )

        self._lbl_distribution_params = self.__create_label(
            master=self._frame_widgets, text="Параметры распределения")
        self._lbl_distribution_params.config(
            font=(self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE), background="#3D517F")
        self._lbl_distribution_params.grid(
            row=6, column=0, columnspan=4, sticky='wens', padx=10, pady=30)

        # default uniform distribution params
        self._frame_distribution_params.set_parameters(
            parameters=[("a"), ("b")]
        )

        self._lbl_input_intervals = self.__create_label(
            master=self._frame_widgets, text="Интервалы вывода графиков")
        self._lbl_input_intervals.config(
            font=(self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE), background="#3D517F")
        self._lbl_input_intervals.grid(
            row=101, column=0, columnspan=4, sticky='wens', padx=10, pady=30)

        self._lbl_input_x_min = self.__create_label(
            master=self._frame_widgets, text="X_min")
        self._lbl_input_x_min.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE), background="#3D517F")
        self._lbl_input_x_min.grid(
            row=102, column=0, columnspan=2, sticky='wens', padx=10, pady=5
        )

        self._entry_input_x_min = self.__create_entry(
            master=self._frame_widgets)
        self._entry_input_x_min.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE), width=20,
        )
        self._entry_input_x_min.grid(
            row=102, column=2, columnspan=2, sticky='wens', padx=10, pady=5
        )

        self._lbl_input_x_max = self.__create_label(
            master=self._frame_widgets, text="X_max")
        self._lbl_input_x_max.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE), background="#3D517F")
        self._lbl_input_x_max.grid(
            row=103, column=0, columnspan=2, sticky='wens', padx=10, pady=5
        )

        self._entry_input_x_max = self.__create_entry(
            master=self._frame_widgets)
        self._entry_input_x_max.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE), width=20,
        )
        self._entry_input_x_max.grid(
            row=103, column=2, columnspan=2, sticky='wens', padx=10, pady=5
        )
        # self._btn_calculate = self.__create_button(
        #     master=self._frame_widgets, text="Вычислить")
        # self._btn_calculate.config(font=(
        #     self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE), background=self.cfgWin.WHITE)
        # self._btn_calculate.config(command=self.__calc_and_display_results)
        # self._btn_calculate.grid(
        #     row=2, column=0, columnspan=4, sticky='wens', padx=10, pady=30)

        # self._btn_gen_random_intens = self.__create_button(
        #     master=self._frame_widgets, text="Сгенерировать")
        # self._btn_gen_random_intens.config(font=(
        #     self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE), command=self.__gen_random_intens, background=self.cfgWin.WHITE)
        # self._btn_gen_random_intens.grid(
        #     row=3, column=0, columnspan=4, sticky='wens', padx=10)

        # self._btn_graph_states_probs = self.__create_button(
        #     self._frame_widgets, "Построить графики\n вероятностей состояний")
        # self._btn_graph_states_probs.config(font=(
        #     self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE), command=self.__plot_probs_states_graphs)
        # self._btn_graph_states_probs.grid(
        #     row=4, column=0, columnspan=4, sticky='wens', padx=10, pady=30)

        # self._lbl_title = self.__create_label(
        #     master=self._frame_results, text="")  # text will appear later
        # self._lbl_title.config(
        #     font=(self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE), background="#b0b0b0")
        # self._lbl_title.pack(pady=30)

        # self._intensity_matrix = Table(master=self._frame_results)
        # self._intensity_matrix.config(background="#b0b0b0")
        # self._intensity_matrix.pack()

        # self._result_table = Table(master=self._frame_results)
        # self._result_table.config(background="#b0b0b0")
        # self._result_table.pack(pady=50)

        # self._lbl_empty = self.__create_label("")
        # self._lbl_empty.config(bg="#3D517F")
        # self._lbl_empty.grid(row=4, column=0, columnspan=4, sticky='wens')

    #
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
    # def __create_display(self, master: tk.Tk | tk.Frame) -> intensity_matrix.Display:
    #     """
    #     Метод создает фрейм для экрана отображения результатов
    #     :return: фрейм для экрана отображения результатов
    #     """

    #     frame_plane = intensity_matrix.Display(
    #         master=master,
    #         background="#b0b0b0",
    #     )

    #     return frame_plane

    def __create_frame(self, master) -> tk.Frame:
        """
        Метод создает фрейм
        """

        frame_widgets = tk.Frame(
            master=master,
            width=self.cfgWin.FRAME_WIDGET_WIDTH,
            background=self.cfgWin.WHITE,
        )

        return frame_widgets

    def __create_label(self, master: tk.Tk | tk.Frame, text: str) -> tk.Label:
        """
        Метод создает label
        """
        label = tk.Label(
            master=master,
            text=text,
            font=(self.cfgWin.FONT, self.cfgWin.FONT_SIZE,
                  self.cfgWin.FONT_STYLE),  # default
            background=self.cfgWin.WHITE,
        )

        return label

    # def __create_button(self, master: tk.Tk | tk.Frame, text: str) -> tk.Button:
    #     """
    #     Метод создает виджет кнопки (button)
    #     :param text:  текст
    #     :return: виджет кнопки
    #     """
    #     button = tk.Button(
    #         master=master,
    #         text=text,
    #         font=(self.cfgWin.FONT, self.cfgWin.FONT_SIZE,
    #               self.cfgWin.FONT_STYLE),  # default
    #         background="#758BBF",
    #         relief=tk.RAISED
    #     )

    #     return button

    def __create_entry(self, master: tk.Tk | tk.Frame) -> tk.Entry:
        """
        Метод создает виджет однострочного поля ввода (entry)
        :return: виджет однострочного поля ввода
        """
        entry = tk.Entry(
            master=master,
            width=self.cfgWin.ENTRY_WIDTH,  # default
            relief=tk.SUNKEN,
            borderwidth=self.cfgWin.ENTRY_BORDER_WIDTH,  # default
            justify=tk.CENTER,
            font=(self.cfgWin.FONT, self.cfgWin.FONT_SIZE,
                  self.cfgWin.FONT_STYLE),  # default
            highlightbackground="#b0b0b0",
            highlightcolor="#b0b0b0"
        )

        return entry

    def __pack_uniform_params(self) -> None:
        """
        Метод упаковывает параметры равномерного распределения
        """

        params = [
            ("a"),
            ("b"),
        ]
        self._frame_distribution_params.set_parameters(parameters=params)

    def __pack_erlang_params(self) -> None:
        """
        Метод упаковывает параметры распределения Эрланга
        """

        params = [
            ("k"),
            ("λ"),
        ]
        self._frame_distribution_params.set_parameters(parameters=params)

    def __pack_poisson_params(self) -> None:
        """
        Метод упаковывает параметры распределения Пуассона
        """

        params = [
            ("λ"),
        ]
        self._frame_distribution_params.set_parameters(parameters=params)

    def __pack_exponential_params(self) -> None:
        """
        Метод упаковывает параметры экспоненциального распределения
        """

        params = [
            ("λ"),
        ]
        self._frame_distribution_params.set_parameters(parameters=params)

    def __pack_normal_params(self) -> None:
        """
        Метод упаковывает параметры нормального распределения
        """

        params = [
            ("μ"),
            ("σ"),
        ]
        self._frame_distribution_params.set_parameters(parameters=params)
    # def __display_intensity_matrix(self, *args):
    #     """
    #     Метод создает и отображает матрицу интенсивностей перехода состояний на экране
    #     """
    #     cnt_states = self._var_input_cnt_states.get()
    #     if not cnt_states:
    #         return

    #     if not self.__check_input_count_states(cnt_states=cnt_states):
    #         messagebox.showwarning(
    #             "Предупреждение", "Ошибка! Необходимо ввести количество состояний -- целое число от 1 до 10")
    #         return

    #     cnt_states = int(cnt_states)

    #     self._lbl_title.config(
    #         text="Матрица интенсивностей переходов состояний")

    #     self._result_table.clear()

    #     self._intensity_matrix.clear()
    #     row_headers = [f"S{i + 1}" for i in range(cnt_states)]
    #     col_headers = [f"S{i + 1}" for i in range(cnt_states)]
    #     self._intensity_matrix.create_and_place_table(
    #         cnt_states, cnt_states, row_headers, col_headers)

    # def __check_input_count_states(self, cnt_states) -> bool:
    #     """
    #     Проверка корректности введенного числа интенсивностей
    #     """
    #     if not checks.check_int(cnt_states):
    #         return False

    #     cnt_states = int(cnt_states)

    #     if cnt_states < 0 or cnt_states > 10:
    #         return False

    #     return True

    # def __calc_and_display_results(self):
    #     """
    #     Метод для подсчета предельных вероятностей и времен
    #     и вывода результатов на экран
    #     """

    #     cnt_states = self._var_input_cnt_states.get()
    #     if not cnt_states:
    #         return

    #     if not self.__check_input_count_states(cnt_states=cnt_states):
    #         messagebox.showwarning(
    #             "Предупреждение", "Ошибка! Необходимо ввести количество состояний -- целое число от 1 до 10")
    #         return

    #     cnt_states = int(cnt_states)

    #     self._result_table.clear()
    #     row_headers = ["P", "T"]
    #     col_headers = [f"S{i + 1}" for i in range(cnt_states)]
    #     self._result_table.create_and_place_table(
    #         2, cnt_states, row_headers, col_headers)

    #     mtr_intens = self.__get_values_from_mtr_entries()
    #     if mtr_intens is None:
    #         return

    #     if self.__mtr_is_empty(mtr_intens):
    #         messagebox.showwarning(
    #             "Предупреждение",
    #             "Сначала заполните матрицу интенсивностей перехода"
    #         )
    #         return

    #     # mtr_intens = [
    #     #     [1.01, 2.95, 3.39],
    #     #     [3.07, 3.71, 3.80],
    #     #     [3.55, 0.02, 0.83]
    #     # ]

    #     # mtr_intens = [
    #     #     [0.0, 0.50, 0.19],
    #     #     [2.0, 0.0, 0.20],
    #     #     [1.0, 3.0, 0.0]
    #     # ]

    #     solver = KolmogorovEqSolver(mtr_intens)

    #     try:
    #         probs, stable_times = solver.solve()
    #     except np.linalg.LinAlgError:
    #         messagebox.showerror(
    #             "Ошибка",
    #             "Невозможно решить систему уравнений"
    #         )
    #         return

    #     probs = list(map(lambda num: f"{num: .3f}", probs))
    #     stable_times = list(map(lambda num: f"{num: .3f}", stable_times))

    #     self._result_table.set_data([probs, stable_times])

    # def __plot_probs_states_graphs(self):
    #     """
    #     Метод для построения графиков вероятностей состояний
    #     """
    #     mtr_intens = self.__get_values_from_mtr_entries()
    #     if mtr_intens is None:
    #         return
    #     # mtr_intens = [
    #     #     [1.01, 2.95, 3.39],
    #     #     [3.07, 3.71, 3.80],
    #     #     [3.55, 0.02, 0.83]
    #     # ]

    #     # mtr_intens = [
    #     #     [0.0, 0.50, 0.19],
    #     #     [2.0, 0.0, 0.20],
    #     #     [1.0, 3.0, 0.0]
    #     # ]

    #     solver = KolmogorovEqSolver(mtr_intens)
    #     try:
    #         probs, stable_times = solver.solve()
    #     except np.linalg.LinAlgError:
    #         messagebox.showerror(
    #             "Ошибка",
    #             "Невозможно решить систему уравнений"
    #         )
    #         return

    #     mtr_coeff = solver.get_mtr_coeff_for_graphs()

    #     t = np.linspace(0, 5, 300)
    #     # начальные условия (в первом состоянии)
    #     y0 = [0 for _ in range(len(probs) - 1)] + [1]

    #     res_ode = integrate.odeint(solver.solve_ode, y0, t, args=(mtr_coeff,))
    #     res_ode = np.transpose(res_ode)

    #     new_window = tk.Toplevel(self)
    #     new_window.title("Графики вероятностей состояний")

    #     # Создаем фигуру и оси
    #     fig, ax = plt.subplots()

    #     # Создаем холст для отображения графика в Tkinter
    #     canvas = FigureCanvasTkAgg(fig, master=new_window)
    #     canvas.draw()
    #     canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    #     for i in range(len(res_ode)):
    #         ax.plot(t, res_ode[i], label=f"P_{i + 1}")

    #     for i in range(len(probs)):
    #         ax.plot(stable_times[i], probs[i], 'ro')

    #     ax.set_xlabel("Время (t)")
    #     ax.set_ylabel("Вероятность P")
    #     ax.set_title("Графики вероятностей состояний")
    #     ax.grid(True)
    #     ax.legend()

    #     # обновляем холст
    #     canvas.draw()

    # def __get_values_from_mtr_entries(self):
    #     """
    #     Метод для получения значений интенсивностей перехода из полей ввода
    #     """
    #     mtr_intens = list()

    #     for i in range(len(self._intensity_matrix.mtr_entries)):
    #         tmp = list()
    #         for j in range(len(self._intensity_matrix.mtr_entries[0])):
    #             value = self._intensity_matrix.mtr_entries[i][j].get().strip()
    #             if not value:
    #                 value = 0
    #             else:
    #                 if checks.check_int(value):
    #                     value = int(value)
    #                 elif checks.check_float(value):
    #                     value = float(value)
    #                 else:
    #                     # print(f"value = |{value}|")

    #                     messagebox.showwarning(
    #                         "Предупреждение",
    #                         f"Ошибка! Интенсивность перехода из состояния S_{i} "
    #                         f"в состояние S_{j} некорректная! Ожидается целое или вещественное положительное число"
    #                     )
    #                     return
    #             tmp.append(value)

    #         mtr_intens.append(tmp)

    #     return mtr_intens

    # def __gen_random_intens(self):
    #     """
    #     Метод позволяет заполнить матрицу интенсивности случайными значениями
    #     """
    #     if len(self._intensity_matrix.mtr_entries) == 0:
    #         messagebox.showwarning(
    #             "Предупреждение",
    #             "Сначала создайте матрицу интенсивностей перехода"
    #         )
    #         return

    #     a = 0.1
    #     b = 10.0

    #     random_intensities = []

    #     for i in range(len(self._intensity_matrix.mtr_entries)):
    #         tmp = []
    #         for j in range(len(self._intensity_matrix.mtr_entries[0])):
    #             tmp.append(f"{random.uniform(a, b): .3f}")

    #         random_intensities.append(tmp)

    #     self._intensity_matrix.set_data(random_intensities)

    # @staticmethod
    # def __mtr_is_empty(mtr):
    #     """
    #     Метод для проверки, является ли двумерный массив нулевым
    #     """

    #     for i in range(len(mtr)):
    #         for j in range(len(mtr[0])):
    #             if mtr[i][j] != 0:
    #                 return False

    #     return True
    # #
    def __create_radiobutton(self, text: str, var) -> tk.Radiobutton:
        """
        Метод создает переключатель
        """
        rbt = tk.Radiobutton(
            self._frame_widgets,
            text=text,
            value=text,
            variable=var,
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE),
            background="#3D517F",
            activebackground="#b0b0b0",
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            relief="flat",
            anchor=tk.W
        )

        return rbt
    #
    # @staticmethod
    # def get_data(entry1: tk.Entry, entry2: tk.Entry) -> (str, str):
    #     """
    #     Метод получает данные с 2-х однострочных полей ввода координат
    #     :param entry1: поле ввода абсциссы
    #     :param entry2: поле вода ординаты
    #     :return: кортеж с данными
    #     """
    #
    #     return entry1.get(), entry2.get()
    #
    # def __get_point(self, entry_x: tk.Entry, entry_y: tk.Entry) -> (int | float, int | float):
    #     """
    #     Метод получает точку с однострочных полей ввода координат
    #     :param entry_x: поле ввода абсциссы
    #     :param entry_y: поле вода ординаты
    #     :return:
    #     """
    #     x, y = self.get_data(entry_x, entry_y)
    #
    #     x = int(x) if self.is_int(x) else float(x) if self.is_float(x) else x
    #     y = int(y) if self.is_int(y) else float(y) if self.is_float(y) else y
    #
    #     return x, y
    #
    # @staticmethod
    # def __check_input_point(x: int | float, y: int | float) -> bool:
    #     """
    #     Метод проверяет введенную точку на корректность
    #     :param x: абсцисса точки
    #     :param y: ордината точки
    #     :return: True, если точка валидная, False иначе
    #     """
    #     if isinstance(x, str) or isinstance(y, str):
    #         text = "Некорректные данные для точки! Попробуйте снова."
    #         messagebox.showwarning("", text)
    #
    #         return False
    #
    #     return True
    #
    # @staticmethod
    # def is_int(x: str) -> bool:
    #     """
    #     Метод проверяет, является ли строка целым числом
    #     :param x: строка
    #     :return: True, если целое число, False иначе
    #     """
    #     if check_int(x):
    #         return True
    #
    #     return False
    #
    # @staticmethod
    # def is_float(x: str) -> bool:
    #     """
    #     Метод проверяет, число ли переданный параметр.
    #     :param x:
    #     :return: True, если число, False иначе
    #     """
    #     if check_float(x):
    #         return True
    #
    #     return False
    #
    # # методы для лабораторной
    #
    # def __draw_func(self, func: Callable[[int | float, int | float], int | float]):
    #     """
    #     Метод позволяет отобразить поверхность для переданной функции
    #     """
    #     x_from = float(self._entry_x_from.get())
    #     x_to = float(self._entry_x_to.get())
    #
    #     z_from = float(self._entry_z_from.get())
    #     z_to = float(self._entry_z_to.get())
    #
    #     x_step = float(self._entry_x_step.get())
    #     z_step = float(self._entry_x_step.get())
    #
    #     # углы все изначально по нулям
    #     self._plane.draw_func([x_from, x_to], [z_from, z_to], x_step, z_step, func)
    #
    # def __create_graph(self):
    #     """
    #     Метод, позволяющий отобразить поверхность
    #     """
    #     match self._rbt_funcs.get():
    #         case "cos(x) * sin(z)":
    #             self.__draw_func(func=f0)
    #         case "sqrt(fabs(x * z))":
    #             self.__draw_func(func=f1)
    #         case "exp(cos(x) * sin(z))":
    #             self.__draw_func(func=f2)
    #         case "sin(x * z)":
    #             self.__draw_func(func=f3)
    #         case _:
    #             print("Не то")
    #
    # def __rotate_func_around_x(self, func: Callable[[int | float, int | float], int | float]):
    #     """
    #     Метод позволяет отобразить поверхность для переданной функции
    #     """
    #     x_from = float(self._entry_x_from.get())
    #     x_to = float(self._entry_x_to.get())
    #
    #     z_from = float(self._entry_z_from.get())
    #     z_to = float(self._entry_z_to.get())
    #
    #     x_step = float(self._entry_x_step.get())
    #     z_step = float(self._entry_x_step.get())
    #
    #     angle_x = float(self._entry_x_rotate.get())
    #
    #     self._plane.rotate_around_x([x_from, x_to], [z_from, z_to], x_step, z_step, func, angle_x)
    #
    # def __rotate_graph_around_x(self):
    #     """
    #     Метод, позволяющий отобразить поверхность
    #     """
    #     match self._rbt_funcs.get():
    #         case "cos(x) * sin(z)":
    #             self.__rotate_func_around_x(func=f0)
    #         case "sqrt(fabs(x * z))":
    #             self.__rotate_func_around_x(func=f1)
    #         case "exp(cos(x) * sin(z))":
    #             self.__rotate_func_around_x(func=f2)
    #         case "sin(x * z)":
    #             self.__rotate_func_around_x(func=f3)
    #         case _:
    #             print("Не то")
    #
    # def __rotate_func_around_y(self, func: Callable[[int | float, int | float], int | float]):
    #     """
    #     Метод позволяет отобразить поверхность для переданной функции
    #     """
    #     x_from = float(self._entry_x_from.get())
    #     x_to = float(self._entry_x_to.get())
    #
    #     z_from = float(self._entry_z_from.get())
    #     z_to = float(self._entry_z_to.get())
    #
    #     x_step = float(self._entry_x_step.get())
    #     z_step = float(self._entry_x_step.get())
    #
    #     angle_y = float(self._entry_x_rotate.get())
    #
    #     self._plane.rotate_around_y([x_from, x_to], [z_from, z_to], x_step, z_step, func, angle_y)
    #
    # def __rotate_graph_around_y(self):
    #     """
    #     Метод, позволяющий отобразить поверхность
    #     """
    #     match self._rbt_funcs.get():
    #         case "cos(x) * sin(z)":
    #             self.__rotate_func_around_y(func=f0)
    #         case "sqrt(fabs(x * z))":
    #             self.__rotate_func_around_y(func=f1)
    #         case "exp(cos(x) * sin(z))":
    #             self.__rotate_func_around_y(func=f2)
    #         case "sin(x * z)":
    #             self.__rotate_func_around_y(func=f3)
    #         case _:
    #             print("Не то")
    #
    # def __rotate_func_around_z(self, func: Callable[[int | float, int | float], int | float]):
    #     """
    #     Метод позволяет отобразить поверхность для переданной функции
    #     """
    #     x_from = float(self._entry_x_from.get())
    #     x_to = float(self._entry_x_to.get())
    #
    #     z_from = float(self._entry_z_from.get())
    #     z_to = float(self._entry_z_to.get())
    #
    #     x_step = float(self._entry_x_step.get())
    #     z_step = float(self._entry_x_step.get())
    #
    #     angle_z = float(self._entry_x_rotate.get())
    #
    #     self._plane.rotate_around_z([x_from, x_to], [z_from, z_to], x_step, z_step, func, angle_z)
    #
    # def __rotate_graph_around_z(self):
    #     """
    #     Метод, позволяющий отобразить поверхность
    #     """
    #     match self._rbt_funcs.get():
    #         case "cos(x) * sin(z)":
    #             self.__rotate_func_around_z(func=f0)
    #         case "sqrt(fabs(x * z))":
    #             self.__rotate_func_around_z(func=f1)
    #         case "exp(cos(x) * sin(z))":
    #             self.__rotate_func_around_z(func=f2)
    #         case "sin(x * z)":
    #             self.__rotate_func_around_z(func=f3)
    #         case _:
    #             print("Не то")
    #
    # # -----------------------------------------------------------------
    #
    # # очистка и справка
    # # -----------------------------------------------------------------
    # def __clean_plane(self) -> None:
    #     """
    #     Метод позволяет очистить содержимое плоскости
    #     """
    #     self._plane.clean_plane()
    #
    # @staticmethod
    # def __print_info() -> None:
    #     """
    #     Метод выводит информацию о программе
    #     """
    #     text = 'С помощью данной программы можно выполнить построение заранее выбранной поверхности ' \
    #            'используя алгоритм плавающего горизонта.\n'
    #
    #     messagebox.showinfo('', text)
