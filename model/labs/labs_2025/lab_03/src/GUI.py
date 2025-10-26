# from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import os
# from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from torch.linalg import solve
from matplotlib.figure import Figure

import config_GUI as cfg

import checks
from distribution_params_frame import DistributionParamsFrame
from distributions import UniformDistribution, PoissonDistribution, ExponentialDistribution, NormalDistribution, ErlangDistribution
from table import Table

# from PointClass import Point

X_COUNT = 1000
ROOT_DIR = "/home/nikitalystsev/Documents/bmstu/sem_07_bmstu/model/labs/labs_2025/"


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

        self.title("Лабораторная №3, Лысцев Никита ИУ7-73Б")

        root_width = 1600
        root_height = 900
        self.geometry(f"{root_width}x{root_height}+0+0")
        self.resizable(width=False, height=False)

        # frames
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

        self._frame_graphs = self.__create_frame(master=self._frame_results)
        self._frame_graphs.config(background="#b0b0b0")
        self._frame_graphs.pack(fill=tk.X)

        # -----------------------------------------------

        # constants
        self._uniform_distribution = "Равномерное распределение"
        self._erlang_distribution = "Распределение Эрланга"
        self._poisson_distribution = "Распределение Пуассона"
        self._exponential_distribution = "Экспоненциальное распределение"
        self._normal_distribution = "Нормальное распределение"

        # distributions
        self._uniform = UniformDistribution(0, 0)  # random params
        self._poisson = PoissonDistribution(0)  # also random param
        self._exponential = ExponentialDistribution(0)  # absolutely random
        self._normal = NormalDistribution(0, 1)  # randomly
        self._erlang = ErlangDistribution(0, 0)  # exactly random
        # -----------------------------------------------

        # widgets
        # -----------------------------------------------
        self._var_choice_distribution_type = tk.StringVar(
            value=self._uniform_distribution
        )

        self._lbl_input_cnt_states = self.__create_label(
            master=self._frame_widgets, text="Законы распределения"
        )
        self._lbl_input_cnt_states.config(
            font=(self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE), background="#3D517F"
        )
        self._lbl_input_cnt_states.grid(
            row=0, column=0, columnspan=4, sticky='wens', padx=10, pady=30
        )

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
            master=self._frame_widgets, text="x_min")
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
            master=self._frame_widgets, text="x_max")
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

        self._btn_calc = self.__create_button(
            self._frame_widgets, "Вычислить"
        )
        self._btn_calc.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE),
            background=self.cfgWin.WHITE,
            command=self.__draw_selected_data
        )
        self._btn_calc.grid(
            row=104, column=0, columnspan=4,
            sticky='wens', padx=10, pady=30
        )

        self._table = Table(master=self._frame_results)
        self._table.config(background="#b0b0b0")
        self._table.pack(pady=30)

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
            foreground=self.cfgWin.WHITE,
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
            activebackground=self.cfgWin.WHITE,
            foreground=self.cfgWin.WHITE,
            borderwidth=0,
            selectcolor=self.cfgWin.BLACK,
            highlightthickness=0,
            bd=0,
            relief="flat",
            anchor=tk.W
        )

        return rbt

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

    def __is_number(self, x: str) -> bool:
        """
        Метод проверка введенного значения на число
        """
        if checks.check_int(x) or checks.check_float(x):
            return True

        return False

    def __get_interval_x_min_x_max(self):
        """
        Метод получает интервал по оси Ox для вывода графиков
        """
        x_min = self._entry_input_x_min.get()
        x_max = self._entry_input_x_max.get()

        if not self.__is_number(x_min) or not self.__is_number(x_max):
            messagebox.showwarning(
                "Ошибка!",
                "Необходимо ввести интервал по оси Ox для вывода графиков"
            )
            return

        _x_min, _x_max = 0, 0

        if checks.check_int(x_min):
            _x_min = int(x_min)
        else:
            _x_min = float(x_min)

        if checks.check_float(x_max):
            _x_max = int(x_max)
        else:
            _x_max = float(x_max)

        if (_x_min >= _x_max):
            messagebox.showwarning(
                "Ошибка!",
                "x_min <= x_max"
            )
            return

        return _x_min, _x_max

    def __get_uniform_a_b(self):
        """
        Метод получает параметры a и b равномерного распределения
        """
        values = self._frame_distribution_params.get_values()
        a = values["a"]
        b = values["b"]

        if not self.__is_number(a) or not self.__is_number(b):
            messagebox.showwarning(
                "Ошибка!",
                "Необходимо ввести параметры a и b равномерного распределения"
            )
            return

        _a, _b = 0, 0

        if checks.check_int(a):
            _a = int(a)
        else:
            _a = float(a)

        if checks.check_float(b):
            _b = int(b)
        else:
            _b = float(b)

        if (_a >= _b):
            messagebox.showwarning(
                "Ошибка!",
                "a <= b"
            )
            return

        return _a, _b

    def __draw_uniform_distribution_graphs(self):
        params = self.__get_uniform_a_b()
        if params is None:
            return

        self._uniform.set_params(*params)

        x_ranges = self.__get_interval_x_min_x_max()
        if x_ranges is None:
            return

        x_min, x_max = x_ranges

        x_list = []
        F_list = []
        f_list = []

        step = (x_max - x_min) / X_COUNT
        x = x_min
        while x <= x_max:
            F_list.append(self._uniform.F(x))
            f_list.append(self._uniform.f(x))
            x_list.append(x)
            x += step

        for widget in self._frame_graphs.winfo_children():
            widget.destroy()

        # Сделаем фигуру шире и включим constrained_layout
        fig = Figure(figsize=(11, 3.5), dpi=100, constrained_layout=False)

        ax1 = fig.add_subplot(121)
        ax1.plot(x_list, F_list)
        ax1.set_title('Функция распределения F(x)')
        ax1.set_xlabel('x')
        ax1.set_ylabel('F(x)', labelpad=8)
        ax1.grid(True)

        ax2 = fig.add_subplot(122)
        ax2.plot(x_list, f_list)
        ax2.set_title('Функция плотности распределения f(x)')
        ax2.set_xlabel('x')
        ax2.set_ylabel('f(x)', labelpad=8)
        ax2.grid(True)

        # поворот xticks если много меток (опционально)
        for ax in (ax1, ax2):
            for lbl in ax.get_xticklabels():
                lbl.set_rotation(0)

        # Явно увеличим горизонтальный промежуток между субплотами
        fig.subplots_adjust(left=0.06, right=0.98, top=0.92,
                            bottom=0.15, wspace=0.35)

        # Сохранение: bbox_inches='tight' чтобы ничего не обрезалось
        save_dir = os.path.join(ROOT_DIR, "lab_03", "data", "uniform")
        os.makedirs(save_dir, exist_ok=True)
        filename = os.path.join(
            save_dir, f"ud_{self._uniform.get_a()}_{self._uniform.get_b()}.svg")
        fig.savefig(filename, format="svg",
                    bbox_inches='tight', pad_inches=0.02)

        # Встраиваем в tkinter Frame
        canvas = FigureCanvasTkAgg(fig, master=self._frame_graphs)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def __draw_uniform_expectation_and_variance(self):
        """
        метод будет создавать таблицу с мат ожиданием и дисперсией случайной величины
        """
        params = self.__get_uniform_a_b()
        if params is None:
            return

        self._uniform.set_params(*params)

        self._table.create_and_place_table(2, 1, ["M[X]", "D[X]"], ["Values"])

        data = [
            [f"{self._uniform.M(): .3f}"],
            [f"{self._uniform.D(): .3f}"]
        ]
        self._table.set_data(data=data)

    def __draw_uniform_data(self):
        """
        Метод выводит данные
        """
        self.__draw_uniform_distribution_graphs()
        self.__draw_uniform_expectation_and_variance()

    def __get_erlang_k_lamb(self):
        """
        Метод получает параметры k и λ распределения Эрланга
        """
        values = self._frame_distribution_params.get_values()
        k = values["k"]
        lamb = values["λ"]

        if not self.__is_number(k) or not self.__is_number(lamb):
            messagebox.showwarning(
                "Ошибка!",
                "Необходимо ввести параметры k и λ распределения Эрланга"
            )
            return

        _k, _lamb = 0, 0

        if checks.check_int(k):
            _k = int(k)
        else:
            messagebox.showerror(
                "Ошибка!",
                "k - целое число"
            )
            return

        if checks.check_float(lamb):
            _lamb = int(lamb)
        else:
            _lamb = float(lamb)

        if (_lamb <= 0):
            messagebox.showwarning(
                "Ошибка!",
                "λ > 0"
            )
            return

        return _k, _lamb

    def __draw_erlang_distribution_graphs(self):
        params = self.__get_erlang_k_lamb()
        if params is None:
            return

        self._erlang.set_params(*params)

        x_ranges = self.__get_interval_x_min_x_max()
        if x_ranges is None:
            return

        x_min, x_max = x_ranges

        x_list = []
        F_list = []
        f_list = []

        step = (x_max - x_min) / X_COUNT
        x = x_min
        while x <= x_max:
            F_list.append(self._erlang.F(x))
            f_list.append(self._erlang.f(x))
            x_list.append(x)
            x += step

        for widget in self._frame_graphs.winfo_children():
            widget.destroy()

        # Сделаем фигуру шире и включим constrained_layout
        fig = Figure(figsize=(11, 3.5), dpi=100, constrained_layout=False)

        ax1 = fig.add_subplot(121)
        ax1.plot(x_list, F_list)
        ax1.set_title('Функция распределения F(x)')
        ax1.set_xlabel('x')
        ax1.set_ylabel('F(x)', labelpad=8)
        ax1.grid(True)

        ax2 = fig.add_subplot(122)
        ax2.plot(x_list, f_list)
        ax2.set_title('Функция плотности распределения f(x)')
        ax2.set_xlabel('x')
        ax2.set_ylabel('f(x)', labelpad=8)
        ax2.grid(True)

        # поворот xticks если много меток (опционально)
        for ax in (ax1, ax2):
            for lbl in ax.get_xticklabels():
                lbl.set_rotation(0)

        # Явно увеличим горизонтальный промежуток между субплотами
        fig.subplots_adjust(left=0.06, right=0.98, top=0.92,
                            bottom=0.15, wspace=0.35)

        # Сохранение: bbox_inches='tight' чтобы ничего не обрезалось
        save_dir = os.path.join(ROOT_DIR, "lab_03", "data", "erlang")
        os.makedirs(save_dir, exist_ok=True)
        filename = os.path.join(
            save_dir, f"erlang_{params[0]}_{params[1]}.svg")
        fig.savefig(filename, format="svg",
                    bbox_inches='tight', pad_inches=0.02)

        # Встраиваем в tkinter Frame
        canvas = FigureCanvasTkAgg(fig, master=self._frame_graphs)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def __draw_erlang_expectation_and_variance(self):
        """
        метод будет создавать таблицу с мат ожиданием и дисперсией случайной величины
        """
        params = self.__get_erlang_k_lamb()
        if params is None:
            return

        self._erlang.set_params(*params)

        self._table.create_and_place_table(2, 1, ["M[X]", "D[X]"], ["Values"])

        data = [
            [f"{self._erlang.M(): .3f}"],
            [f"{self._erlang.D(): .3f}"]
        ]
        self._table.set_data(data=data)

    def __draw_erlang_data(self):
        """
        Метод выводит данные
        """
        self.__draw_erlang_distribution_graphs()
        self.__draw_erlang_expectation_and_variance()

    def __get_poisson_lamb(self):
        """
        Метод получает параметр λ распределения Пуассона
        """
        values = self._frame_distribution_params.get_values()
        lamb = values["λ"]

        if not self.__is_number(lamb):
            messagebox.showwarning(
                "Ошибка!",
                "Необходимо ввести параметр λ распределения Пуассона"
            )
            return

        _lamb = 0

        if checks.check_int(lamb):
            _lamb = int(lamb)
        else:
            _lamb = float(lamb)

        if (_lamb <= 0):
            messagebox.showwarning(
                "Ошибка!",
                "λ > 0"
            )
            return

        return _lamb

    # def __draw_poisson_distribution_graphs(self):
    #     lamb = self.__get_poisson_lamb()
    #     if lamb is None:
    #         return

    #     self._poisson.set_lambda(lamb)

    #     x_ranges = self.__get_interval_x_min_x_max()
    #     if x_ranges is None:
    #         return

    #     x_min, x_max = x_ranges
    #     x_min = max(0, int(x_min))  # Пуассон >= 0
    #     x_max = int(x_max)

    #     x_list = list(range(x_min, x_max + 1))
    #     cdf_list = [self._poisson.F(x) for x in x_list]
    #     pmf_list = [self._poisson.p(x) for x in x_list]

    #     for widget in self._frame_graphs.winfo_children():
    #         widget.destroy()

    #     fig = Figure(figsize=(11, 3.5), dpi=100, constrained_layout=False)

    #     # CDF график (ступенчатый)
    #     ax1 = fig.add_subplot(121)
    #     ax1.step(x_list, cdf_list, where='post')
    #     ax1.set_title('Функция распределения F(x)')
    #     ax1.set_xlabel('x')
    #     ax1.set_ylabel('F(x)', labelpad=8)
    #     ax1.grid(True)

    #     # PMF график (дискретные точки)
    #     ax2 = fig.add_subplot(122)
    #     ax2.scatter(x_list, pmf_list, color='red', s=40)  # s — размер точек
    #     ax2.set_title('Функция вероятности p(x)')
    #     ax2.set_xlabel('x')
    #     ax2.set_ylabel('P(X=x)', labelpad=8)
    #     ax2.grid(True, axis='y')

    #     fig.subplots_adjust(left=0.06, right=0.98, top=0.92,
    #                         bottom=0.15, wspace=0.35)

    #     save_dir = os.path.join(ROOT_DIR, "lab_03", "data", "poisson")
    #     os.makedirs(save_dir, exist_ok=True)
    #     filename = os.path.join(save_dir, f"poisson_{lamb}.svg")
    #     fig.savefig(filename, format="svg",
    #                 bbox_inches='tight', pad_inches=0.02)

    #     canvas = FigureCanvasTkAgg(fig, master=self._frame_graphs)
    #     canvas.draw()
    #     canvas.get_tk_widget().pack(fill="both", expand=True)

    def __draw_poisson_distribution_graphs(self):
        lamb = self.__get_poisson_lamb()
        if lamb is None:
            return

        self._poisson.set_lambda(lamb)

        x_ranges = self.__get_interval_x_min_x_max()
        if x_ranges is None:
            return

        x_min, x_max = x_ranges
        x_min = max(0, int(x_min))  # Пуассон >= 0
        x_max = int(x_max)

        x_list = list(range(x_min, x_max + 1))
        pmf_list = [self._poisson.p(x) for x in x_list]
        cdf_list = [self._poisson.F(x) for x in x_list]

        for widget in self._frame_graphs.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(11, 3.5), dpi=100, constrained_layout=False)

        # --- CDF (ступенчатый, дискретный) ---
        ax1 = fig.add_subplot(121)
        # чтобы ступеньки корректно доходили до следующего целого, дополним точки правой границей
        x_step = x_list + [x_list[-1] + 1]
        cdf_step = cdf_list + [cdf_list[-1]]
        ax1.step(x_step, cdf_step, where='post')
        ax1.set_title('Функция распределения F(x)')
        ax1.set_xlabel('x')
        ax1.set_ylabel('F(x)', labelpad=8)
        ax1.set_xticks(x_list)            # целочисленные метки
        ax1.set_xlim(x_min - 0.5, x_max + 0.5)
        ax1.set_ylim(0.0, 1.05)
        ax1.grid(True)

        # --- PMF (точки) ---
        ax2 = fig.add_subplot(122)
        ax2.scatter(x_list, pmf_list, color='red', s=50, zorder=3)
        # можно добавить соединяющую пунктирную линию, чтобы визуально не "плавало"
        ax2.plot(x_list, pmf_list, linestyle='dotted', color='gray', zorder=2)

        ax2.set_title('Функция вероятности p(x)')
        ax2.set_xlabel('x')
        ax2.set_ylabel('P(X=x)', labelpad=8)
        ax2.set_xticks(x_list)
        ax2.set_xlim(x_min - 0.5, x_max + 0.5)
        ax2.grid(True, axis='y', linestyle='--', alpha=0.6)

        fig.subplots_adjust(left=0.06, right=0.98, top=0.92,
                            bottom=0.15, wspace=0.35)

        save_dir = os.path.join(ROOT_DIR, "lab_03", "data", "poisson")
        os.makedirs(save_dir, exist_ok=True)
        filename = os.path.join(save_dir, f"poisson_{lamb}.svg")
        fig.savefig(filename, format="svg",
                    bbox_inches='tight', pad_inches=0.02)

        canvas = FigureCanvasTkAgg(fig, master=self._frame_graphs)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def __draw_poisson_expectation_and_variance(self):
        """
        метод будет создавать таблицу с мат ожиданием и дисперсией случайной величины
        """
        lamb = self.__get_poisson_lamb()
        if lamb is None:
            return

        self._poisson.set_lambda(lamb)

        self._table.create_and_place_table(2, 1, ["M[X]", "D[X]"], ["Values"])

        data = [
            [f"{self._poisson.M(): .3f}"],
            [f"{self._poisson.D(): .3f}"]
        ]
        self._table.set_data(data=data)

    def __draw_poissom_data(self):
        """
        Метод выводит данные
        """
        self.__draw_poisson_distribution_graphs()
        self.__draw_poisson_expectation_and_variance()

    def __get_exponential_lamb(self):
        """
        Метод получает параметр λ экспоненциального распределения
        """
        values = self._frame_distribution_params.get_values()
        lamb = values["λ"]

        if not self.__is_number(lamb):
            messagebox.showwarning(
                "Ошибка!",
                "Необходимо ввести параметр λ экспоненциального распределения"
            )
            return

        _lamb = 0

        if checks.check_int(lamb):
            _lamb = int(lamb)
        else:
            _lamb = float(lamb)

        if (_lamb <= 0):
            messagebox.showwarning(
                "Ошибка!",
                "λ > 0"
            )
            return

        return _lamb

    def __draw_exponential_distribution_graphs(self):
        lamb = self.__get_exponential_lamb()
        if lamb is None:
            return

        self._exponential.set_lambda(lamb)

        x_ranges = self.__get_interval_x_min_x_max()
        if x_ranges is None:
            return

        x_min, x_max = x_ranges

        x_list = []
        F_list = []
        f_list = []

        step = (x_max - x_min) / X_COUNT
        x = x_min
        while x <= x_max:
            F_list.append(self._exponential.F(x))
            f_list.append(self._exponential.f(x))
            x_list.append(x)
            x += step

        for widget in self._frame_graphs.winfo_children():
            widget.destroy()

        # Сделаем фигуру шире и включим constrained_layout
        fig = Figure(figsize=(11, 3.5), dpi=100, constrained_layout=False)

        ax1 = fig.add_subplot(121)
        ax1.plot(x_list, F_list)
        ax1.set_title('Функция распределения F(x)')
        ax1.set_xlabel('x')
        ax1.set_ylabel('F(x)', labelpad=8)
        ax1.grid(True)

        ax2 = fig.add_subplot(122)
        ax2.plot(x_list, f_list)
        ax2.set_title('Функция плотности распределения f(x)')
        ax2.set_xlabel('x')
        ax2.set_ylabel('f(x)', labelpad=8)
        ax2.grid(True)

        # поворот xticks если много меток (опционально)
        for ax in (ax1, ax2):
            for lbl in ax.get_xticklabels():
                lbl.set_rotation(0)

        # Явно увеличим горизонтальный промежуток между субплотами
        fig.subplots_adjust(left=0.06, right=0.98, top=0.92,
                            bottom=0.15, wspace=0.35)

        # Сохранение: bbox_inches='tight' чтобы ничего не обрезалось
        save_dir = os.path.join(ROOT_DIR, "lab_03", "data", "exponential")
        os.makedirs(save_dir, exist_ok=True)
        filename = os.path.join(
            save_dir, f"exp_{lamb}.svg")
        fig.savefig(filename, format="svg",
                    bbox_inches='tight', pad_inches=0.02)

        # Встраиваем в tkinter Frame
        canvas = FigureCanvasTkAgg(fig, master=self._frame_graphs)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def __draw_exponential_expectation_and_variance(self):
        """
        метод будет создавать таблицу с мат ожиданием и дисперсией случайной величины
        """
        lamb = self.__get_exponential_lamb()
        if lamb is None:
            return

        self._exponential.set_lambda(lamb)

        self._table.create_and_place_table(2, 1, ["M[X]", "D[X]"], ["Values"])

        data = [
            [f"{self._exponential.M(): .3f}"],
            [f"{self._exponential.D(): .3f}"]
        ]
        self._table.set_data(data=data)

    def __draw_exponential_data(self):
        """
        Метод выводит данные
        """
        self.__draw_exponential_distribution_graphs()
        self.__draw_exponential_expectation_and_variance()

    def __get_normal_mu_sigma(self):
        """
        Метод получает параметры μ и σ нормального распределения
        """
        values = self._frame_distribution_params.get_values()
        mu = values["μ"]
        sigma = values["σ"]

        if not self.__is_number(mu) or not self.__is_number(sigma):
            messagebox.showwarning(
                "Ошибка!",
                "Необходимо ввести параметры μ и σ нормального распределения"
            )
            return

        _mu, _sigma = 0, 0

        if checks.check_int(mu):
            _mu = int(mu)
        else:
            _mu = float(mu)

        if checks.check_float(sigma):
            _sigma = int(sigma)
        else:
            _sigma = float(sigma)

        if (_sigma <= 0):
            messagebox.showwarning(
                "Ошибка!",
                "σ > 0"
            )
            return

        return _mu, _sigma

    def __draw_normal_distribution_graphs(self):
        params = self.__get_normal_mu_sigma()
        if params is None:
            return

        self._normal.set_params(*params)

        x_ranges = self.__get_interval_x_min_x_max()
        if x_ranges is None:
            return

        x_min, x_max = x_ranges

        x_list = []
        F_list = []
        f_list = []

        step = (x_max - x_min) / X_COUNT
        x = x_min
        while x <= x_max:
            F_list.append(self._normal.F(x))
            f_list.append(self._normal.f(x))
            x_list.append(x)
            x += step

        for widget in self._frame_graphs.winfo_children():
            widget.destroy()

        # Сделаем фигуру шире и включим constrained_layout
        fig = Figure(figsize=(11, 3.5), dpi=100, constrained_layout=False)

        ax1 = fig.add_subplot(121)
        ax1.plot(x_list, F_list)
        ax1.set_title('Функция распределения F(x)')
        ax1.set_xlabel('x')
        ax1.set_ylabel('F(x)', labelpad=8)
        ax1.grid(True)

        ax2 = fig.add_subplot(122)
        ax2.plot(x_list, f_list)
        ax2.set_title('Функция плотности распределения f(x)')
        ax2.set_xlabel('x')
        ax2.set_ylabel('f(x)', labelpad=8)
        ax2.grid(True)

        # поворот xticks если много меток (опционально)
        for ax in (ax1, ax2):
            for lbl in ax.get_xticklabels():
                lbl.set_rotation(0)

        # Явно увеличим горизонтальный промежуток между субплотами
        fig.subplots_adjust(left=0.06, right=0.98, top=0.92,
                            bottom=0.15, wspace=0.35)

        # Сохранение: bbox_inches='tight' чтобы ничего не обрезалось
        save_dir = os.path.join(ROOT_DIR, "lab_03", "data", "normal")
        os.makedirs(save_dir, exist_ok=True)
        filename = os.path.join(
            save_dir, f"normal_{params[0]}_{params[1]}.svg")
        fig.savefig(filename, format="svg",
                    bbox_inches='tight', pad_inches=0.02)

        # Встраиваем в tkinter Frame
        canvas = FigureCanvasTkAgg(fig, master=self._frame_graphs)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def __draw_normal_expectation_and_variance(self):
        """
        метод будет создавать таблицу с мат ожиданием и дисперсией случайной величины
        """
        params = self.__get_normal_mu_sigma()
        if params is None:
            return

        self._normal.set_params(*params)

        self._table.create_and_place_table(2, 1, ["M[X]", "D[X]"], ["Values"])

        data = [
            [f"{self._normal.M(): .3f}"],
            [f"{self._normal.D(): .3f}"]
        ]
        self._table.set_data(data=data)

    def __draw_normal_data(self):
        """
        Метод выводит данные
        """
        self.__draw_normal_distribution_graphs()
        self.__draw_normal_expectation_and_variance()

    def __draw_selected_data(self):
        """
        Метод для отображения данных для выбранного закона распределения
        """

        distribution_type = self._var_choice_distribution_type.get()

        match distribution_type:
            case self._uniform_distribution:
                self.__draw_uniform_data()
            case self._erlang_distribution:
                self.__draw_erlang_data()
            case self._poisson_distribution:
                self.__draw_poissom_data()
            case self._exponential_distribution:
                self.__draw_exponential_data()
            case self._normal_distribution:
                self.__draw_normal_data()
            case _:
                messagebox.showwarning(
                    "Ошибка!",
                    "Выбран неизвестный закон распределения!"
                )
