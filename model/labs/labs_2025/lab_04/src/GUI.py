
from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk

import config_GUI as cfg

from distribution_params_frame import DistributionParamsFrame
from queue_system_components.distributions import UniformDistribution, PoissonDistribution, ExponentialDistribution, NormalDistribution, ErlangDistribution
from queue_system_params_frame import QueueSystemParamsFrame

from queue_system_components.time_advance_algs import EventApproach, DeltaTApproach
from queue_system_components.generator import Generator
from queue_system_components.server import Server
from queue_system_components.buffer_memory import BufferMemory

from table import Table

import checks


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

        self.title("Лабораторная №4, Лысцев Никита ИУ7-73Б")

        self.update_idletasks()

        root_width = 1920
        root_height = 996 - 36

        self.geometry(f"{root_width}x{root_height}+0+0")
        self.resizable(width=False, height=False)

        # frames
        # -----------------------------------------------
        self._frame_widgets = self.__create_frame(master=self)
        self._frame_widgets.config(bg="#3D517F", width=400)
        self._frame_widgets.columnconfigure(1, weight=1)
        self._frame_widgets.pack(side=tk.LEFT, fill="both", expand=True)

        self._frame_generator_distribution_params = DistributionParamsFrame(
            self._frame_widgets)
        self._frame_generator_distribution_params.config(background="#3D517F")
        self._frame_generator_distribution_params.grid(
            row=4, column=0, columnspan=4, sticky='wens')

        self._frame_server_distribution_params = DistributionParamsFrame(
            self._frame_widgets)
        self._frame_server_distribution_params.config(background="#3D517F")
        self._frame_server_distribution_params.grid(
            row=9, column=0, columnspan=4, sticky='wens')

        self._frame_time_advance_params = DistributionParamsFrame(
            self._frame_widgets)
        self._frame_time_advance_params.config(background="#3D517F")
        self._frame_time_advance_params.grid(
            row=13, column=0, columnspan=4, sticky='wens')

        self._frame_queue_system_params = QueueSystemParamsFrame(
            self._frame_widgets)
        self._frame_queue_system_params.config(background="#3D517F")
        self._frame_queue_system_params.grid(
            row=15, column=2, rowspan=2, columnspan=2, sticky='wens')

        self._frame_count_tasks = DistributionParamsFrame(
            self._frame_widgets)
        self._frame_count_tasks.config(background="#3D517F")
        self._frame_count_tasks.grid(
            row=17, column=0, columnspan=2, sticky='wens', pady=10
        )

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

        self._disctributions = (
            self._uniform_distribution,
            self._erlang_distribution,
            self._poisson_distribution,
            self._exponential_distribution,
            self._normal_distribution,
        )

        self._delta_t_approach = "Принцип Δt"
        self._event_approach = "Событийный принцип"

        self._time_advance_algs = (
            self._delta_t_approach,
            self._event_approach
        )

        self._with_feedback = "С обратной связью"
        self._without_feedback = "Без обратной связи"

        self._queue_system_types = (
            self._with_feedback,
            self._without_feedback
        )

        # distributions
        self._uniform = UniformDistribution(0, 0)  # random params
        self._poisson = PoissonDistribution(0)  # also random param
        self._exponential = ExponentialDistribution(0)  # absolutely random
        self._normal = NormalDistribution(0, 1)  # randomly
        self._erlang = ErlangDistribution(0, 0)  # exactly random

        # -----------------------------------------------

        # widgets
        # -----------------------------------------------
        # generator
        self._var_choose_generator_distribution_type = tk.StringVar(
            value=self._uniform_distribution
        )

        self._lbl_generator = self.__create_label(
            master=self._frame_widgets, text="Генератор"
        )
        self._lbl_generator.config(
            font=(self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE), background="#3D517F"
        )
        self._lbl_generator.grid(
            row=0, column=0, columnspan=4, sticky='wens', padx=10, pady=15
        )

        self._lbl_generator_distribution = self.__create_label(
            master=self._frame_widgets, text="Закон распределения генератора: "
        )
        self._lbl_generator_distribution.config(
            background="#3D517F",
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE),
            anchor="w",
        )
        self._lbl_generator_distribution.grid(
            row=1, column=0, columnspan=4, sticky='wens', padx=10, pady=5,
        )

        self._combobox_generator_style = ttk.Style()
        self._combobox_generator_style.theme_use('clam')
        self._combobox_generator_style.configure(
            "Custom.TCombobox",
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE),
        )
        self.option_add("*Listbox*Font", (self.cfgWin.FONT,
                        18, self.cfgWin.FONT_STYLE))

        self._combobox_generator = ttk.Combobox(
            master=self._frame_widgets,
            values=self._disctributions,
            style="Custom.TCombobox",
            state="readonly",
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE),
            textvariable=self._var_choose_generator_distribution_type
        )
        # default generator uniform distribution params
        self._frame_generator_distribution_params.set_parameters(
            parameters=[("a"), ("b")]
        )

        self._combobox_generator.bind(
            "<<ComboboxSelected>>", self._pack_chosen_generator_params
        )
        self._combobox_generator.grid(
            row=2, column=0, columnspan=4, sticky='wens', padx=10, pady=5
        )

        self._lbl_generator_distribution_params = self.__create_label(
            master=self._frame_widgets, text="Параметры распределения генератора: "
        )
        self._lbl_generator_distribution_params.config(
            background="#3D517F",
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE),
        )
        self._lbl_generator_distribution_params.grid(
            row=3, column=0, columnspan=4, sticky='wens', padx=10, pady=5,
        )
        ######################################################################

        # server
        self._var_choose_server_distribution_type = tk.StringVar(
            value=self._uniform_distribution
        )

        self._lbl_server = self.__create_label(
            master=self._frame_widgets, text="Обслуживающий аппарат (ОА)"
        )
        self._lbl_server.config(
            font=(self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE), background="#3D517F"
        )
        self._lbl_server.grid(
            row=5, column=0, columnspan=4, sticky='wens', padx=10, pady=15
        )

        self._lbl_server_distribution = self.__create_label(
            master=self._frame_widgets, text="Закон распределения ОА: "
        )
        self._lbl_server_distribution.config(
            background="#3D517F",
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE),
            anchor="w",
        )
        self._lbl_server_distribution.grid(
            row=6, column=0, columnspan=4, sticky='wens', padx=10, pady=5,
        )

        self._combobox_server = ttk.Combobox(
            master=self._frame_widgets,
            values=self._disctributions,
            style="Custom.TCombobox",
            state="readonly",
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE),
            textvariable=self._var_choose_server_distribution_type
        )
        # default generator uniform distribution params
        self._frame_server_distribution_params.set_parameters(
            parameters=[("a"), ("b")]
        )

        self._combobox_server.bind(
            "<<ComboboxSelected>>", self._pack_chosen_server_params
        )
        self._combobox_server.grid(
            row=7, column=0, columnspan=4, sticky='wens', padx=10, pady=5
        )

        self._lbl_server_distribution_params = self.__create_label(
            master=self._frame_widgets, text="Параметры распределения ОА: "
        )
        self._lbl_server_distribution_params.config(
            background="#3D517F",
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE),
        )
        self._lbl_server_distribution_params.grid(
            row=8, column=0, columnspan=4, sticky='wens', padx=10, pady=5,
        )
        ######################################################################

        # time advance
        self._var_choose_time_advance_alg = tk.StringVar(
            value=self._delta_t_approach
        )

        self._lbl_time_advance = self.__create_label(
            master=self._frame_widgets, text="Протяжка модельного времени"
        )
        self._lbl_time_advance.config(
            font=(self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE), background="#3D517F"
        )
        self._lbl_time_advance.grid(
            row=10, column=0, columnspan=4, sticky='wens', padx=10, pady=15
        )

        self._lbl_time_advance_alg = self.__create_label(
            master=self._frame_widgets, text="Алгоритм протяжки модельного времени: "
        )
        self._lbl_time_advance_alg.config(
            background="#3D517F",
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE),
            anchor="w",
        )
        self._lbl_time_advance_alg.grid(
            row=11, column=0, columnspan=4, sticky='wens', padx=10, pady=5,
        )

        self._combobox_time_advance_alg = ttk.Combobox(
            master=self._frame_widgets,
            values=self._time_advance_algs,
            style="Custom.TCombobox",
            state="readonly",
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE),
            textvariable=self._var_choose_time_advance_alg
        )
        # default time advance params
        self._frame_time_advance_params.set_parameters(
            parameters=[("Δt")]
        )

        self._combobox_time_advance_alg.bind(
            "<<ComboboxSelected>>", self._pack_chosen_time_advance_params
        )
        self._combobox_time_advance_alg.grid(
            row=12, column=0, columnspan=4, sticky='wens', padx=10, pady=5
        )
        ######################################################################

        # type of Q-system
        self._var_choose_queue_system_type = tk.StringVar(
            value=self._with_feedback
        )

        self._lbl_queue_system = self.__create_label(
            master=self._frame_widgets, text="Система массового обслуживания (СМО)"
        )
        self._lbl_queue_system.config(
            font=(self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE), background="#3D517F"
        )
        self._lbl_queue_system.grid(
            row=14, column=0, columnspan=4, sticky='wens', padx=10, pady=15
        )

        self._lbl_queue_system_type = self.__create_label(
            master=self._frame_widgets, text="Тип СМО: "
        )
        self._lbl_queue_system_type.config(
            background="#3D517F",
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE),
            anchor="w",
        )
        self._lbl_queue_system_type.grid(
            row=15, column=0, columnspan=2, sticky='wens', padx=10, pady=5,
        )

        self._combobox_queue_system_type = ttk.Combobox(
            master=self._frame_widgets,
            values=self._queue_system_types,
            style="Custom.TCombobox",
            state="readonly",
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE),
            textvariable=self._var_choose_queue_system_type
        )
        # default time advance params
        self._frame_queue_system_params.set_parameters(
            parameters=[("Процент возврата")]
        )

        self._frame_count_tasks.set_parameters(
            parameters=[("Число заявок")]
        )

        self._combobox_queue_system_type.bind(
            "<<ComboboxSelected>>", self._pack_chosen_queue_system_params
        )
        self._combobox_queue_system_type.grid(
            row=16, column=0, columnspan=2, sticky='wens', padx=10, pady=5
        )

        self._btn_calc = self.__create_button(
            self._frame_widgets, "Моделировать"
        )
        self._btn_calc.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE),
            background=self.cfgWin.WHITE,
            command=self.__run_simulation
        )
        self._btn_calc.grid(
            row=17, column=2, columnspan=2,
            sticky='wens', padx=10, pady=15
        )

        self._table = Table(master=self._frame_results)
        self._table.config(background="#b0b0b0")
        self._table.pack(pady=15)

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

    # def __create_radiobutton(self, text: str, var) -> tk.Radiobutton:
    #     """
    #     Метод создает переключатель
    #     """
    #     rbt = tk.Radiobutton(
    #         self._frame_widgets,
    #         text=text,
    #         value=text,
    #         variable=var,
    #         font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE),
    #         background="#3D517F",
    #         activebackground=self.cfgWin.WHITE,
    #         foreground=self.cfgWin.WHITE,
    #         borderwidth=0,
    #         selectcolor=self.cfgWin.BLACK,
    #         highlightthickness=0,
    #         bd=0,
    #         relief="flat",
    #         anchor=tk.W
    #     )

    #     return rbt

    def __pack_uniform_params(self, frame) -> None:
        """
        Метод упаковывает параметры равномерного распределения
        """

        params = [
            ("a"),
            ("b"),
        ]
        frame.set_parameters(parameters=params)

    def __pack_erlang_params(self, frame) -> None:
        """
        Метод упаковывает параметры распределения Эрланга
        """

        params = [
            ("k"),
            ("λ"),
        ]
        frame.set_parameters(parameters=params)

    def __pack_poisson_params(self, frame) -> None:
        """
        Метод упаковывает параметры распределения Пуассона
        """

        params = [
            ("λ"),
        ]
        frame.set_parameters(parameters=params)

    def __pack_exponential_params(self, frame) -> None:
        """
        Метод упаковывает параметры экспоненциального распределения
        """

        params = [
            ("λ"),
        ]
        frame.set_parameters(parameters=params)

    def __pack_normal_params(self, frame) -> None:
        """
        Метод упаковывает параметры нормального распределения
        """

        params = [
            ("μ"),
            ("σ"),
        ]
        frame.set_parameters(parameters=params)

    def __pack_delta_t_params(self) -> None:
        """
        Метод упаковывает параметры принципа Δt
        """

        params = [
            ("Δt"),
        ]
        self._frame_time_advance_params.set_parameters(parameters=params)

    def __pack_queue_system_params(self):
        """
        Метод упаковывает поле ввода для процента возвратов
        """
        params = [
            ("Процент возврата:"),
        ]
        self._frame_queue_system_params.set_parameters(parameters=params)

    def _pack_chosen_generator_params(self, event):
        """
        Метод выводит поля для ввода параметров выбранного закона распределения
        """
        generator_distribution_type = self._var_choose_generator_distribution_type.get()

        match generator_distribution_type:
            case self._uniform_distribution:
                self.__pack_uniform_params(
                    self._frame_generator_distribution_params)
            case self._erlang_distribution:
                self.__pack_erlang_params(
                    self._frame_generator_distribution_params)
            case self._poisson_distribution:
                self.__pack_poisson_params(
                    self._frame_generator_distribution_params)
            case self._exponential_distribution:
                self.__pack_exponential_params(
                    self._frame_generator_distribution_params)
            case self._normal_distribution:
                self.__pack_normal_params(
                    self._frame_generator_distribution_params)
            case _:
                messagebox.showwarning(
                    "Ошибка!",
                    "Выбран неизвестный закон распределения!"
                )

    def _pack_chosen_server_params(self, event):
        """
        Метод выводит поля для ввода параметров выбранного закона распределения
        """
        server_distribution_type = self._var_choose_server_distribution_type.get()

        match server_distribution_type:
            case self._uniform_distribution:
                self.__pack_uniform_params(
                    self._frame_server_distribution_params)
            case self._erlang_distribution:
                self.__pack_erlang_params(
                    self._frame_server_distribution_params)
            case self._poisson_distribution:
                self.__pack_poisson_params(
                    self._frame_server_distribution_params)
            case self._exponential_distribution:
                self.__pack_exponential_params(
                    self._frame_server_distribution_params)
            case self._normal_distribution:
                self.__pack_normal_params(
                    self._frame_server_distribution_params)
            case _:
                messagebox.showwarning(
                    "Ошибка!",
                    "Выбран неизвестный закон распределения!"
                )

    def _pack_chosen_time_advance_params(self, event):
        """
        Метод выводит поля для ввода параметров алгоритмов протяжка модельного времени
        """
        time_advance_alg = self._var_choose_time_advance_alg.get()

        match time_advance_alg:
            case self._delta_t_approach:
                self.__pack_delta_t_params()
            case self._event_approach:
                pass
            case _:
                messagebox.showwarning(
                    "Ошибка!",
                    "Выбран неизвестный закон распределения!"
                )

    def _pack_chosen_queue_system_params(self, event):
        """
        Метод выводит поле ввода для процента возвратов
        """
        queue_system_type = self._var_choose_queue_system_type.get()

        match queue_system_type:
            case self._with_feedback:
                self.__pack_queue_system_params()
            case self._without_feedback:
                self._frame_queue_system_params.clear()
            case _:
                messagebox.showwarning(
                    "Ошибка!",
                    "Выбран неизвестный закон распределения!"
                )

    def __create_uniform_generator(self):
        """
        Метод создает генератор с равномерным распределением
        """
        params = self.__get_uniform_a_b(
            self._frame_generator_distribution_params
        )
        if params is None:
            return

        self._uniform.set_params(*params)

        return Generator(self._uniform)

    def __create_erlang_generator(self):
        """
        Метод создает генератор с распределением Эрланга
        """
        params = self.__get_erlang_k_lamb(
            self._frame_generator_distribution_params
        )
        if params is None:
            return

        self._erlang.set_params(*params)

        return Generator(self._erlang)

    def __create_poisson_generator(self):
        """
        Метод создает генератор с распределением Пуассона
        """
        params = self.__get_poisson_lamb(
            self._frame_generator_distribution_params
        )
        if params is None:
            return

        self._poisson.set_lambda(params)

        return Generator(self._poisson)

    def __create_exponential_generator(self):
        """
        Метод создает генератор с экспоненциальным распределением
        """
        params = self.__get_exponential_lamb(
            self._frame_generator_distribution_params
        )
        if params is None:
            return

        self._exponential.set_lambda(params)

        return Generator(self._exponential)

    def __create_normal_generator(self):
        """
        Метод создает генератор с нормальным распределением
        """
        params = self.__get_normal_mu_sigma(
            self._frame_generator_distribution_params
        )
        if params is None:
            return

        self._normal.set_params(*params)

        return Generator(self._normal)

    def __create_generator(self):
        """
        Метод создает генератор заявок
        """

        generator = None

        generator_distribution_type = self._var_choose_generator_distribution_type.get()

        match generator_distribution_type:
            case self._uniform_distribution:
                generator = self.__create_uniform_generator()
            case self._erlang_distribution:
                generator = self.__create_erlang_generator()
            case self._poisson_distribution:
                generator = self.__create_poisson_generator()
            case self._exponential_distribution:
                generator = self.__create_exponential_generator()
            case self._normal_distribution:
                generator = self.__create_normal_generator()
            case _:
                messagebox.showwarning(
                    "Ошибка!",
                    "Выбран неизвестный закон распределения!"
                )

        if not generator:
            messagebox.showwarning(
                "Ошибка!",
                "Генератор заявок не был успешно создан!"
            )

        return generator

    def __create_uniform_server(self):
        """
        Метод создает ОА с равномерным распределением
        """
        params = self.__get_uniform_a_b(
            self._frame_server_distribution_params
        )
        if params is None:
            return

        self._uniform.set_params(*params)

        return Server(self._uniform)

    def __create_erlang_server(self):
        """
        Метод создает ОА с распределением Эрланга
        """
        params = self.__get_erlang_k_lamb(
            self._frame_server_distribution_params
        )
        if params is None:
            return

        self._erlang.set_params(*params)

        return Server(self._erlang)

    def __create_poisson_server(self):
        """
        Метод создает ОА с распределением Пуассона
        """
        params = self.__get_poisson_lamb(
            self._frame_server_distribution_params
        )
        if params is None:
            return

        self._poisson.set_lambda(params)

        return Server(self._poisson)

    def __create_exponential_server(self):
        """
        Метод создает ОА с экспоненциальным распределением
        """
        params = self.__get_exponential_lamb(
            self._frame_server_distribution_params
        )
        if params is None:
            return

        self._exponential.set_lambda(params)

        return Server(self._exponential)

    def __create_normal_server(self):
        """
        Метод создает ОА с нормальным распределением
        """
        params = self.__get_normal_mu_sigma(
            self._frame_server_distribution_params
        )
        if params is None:
            return

        self._normal.set_params(*params)

        return Server(self._normal)

    def __create_server(self):
        """
        Метод создает ОА для заявок
        """

        server = None

        server_distribution_type = self._var_choose_server_distribution_type.get()

        match server_distribution_type:
            case self._uniform_distribution:
                server = self.__create_uniform_server()
            case self._erlang_distribution:
                server = self.__create_erlang_server()
            case self._poisson_distribution:
                server = self.__create_poisson_server()
            case self._exponential_distribution:
                server = self.__create_exponential_server()
            case self._normal_distribution:
                server = self.__create_normal_server()
            case _:
                messagebox.showwarning(
                    "Ошибка!",
                    "Выбран неизвестный закон распределения!"
                )

        if not server:
            messagebox.showwarning(
                "Ошибка!",
                "ОА для заявок не был успешно создан!"
            )

        return server

    def __get_count_tasks(self):
        """
        Метод позволяет получить необходимое для обслуживания количество заявок
        """
        values = self._frame_count_tasks.get_values()
        count_tasks = values["Число заявок"]

        if not self.__is_number(count_tasks):
            messagebox.showwarning(
                "Ошибка!",
                "Необходимо ввести целое число --- количество заявок на обслуживание"
            )
            return

        _count_tasks = 0

        if checks.check_int(count_tasks):
            _count_tasks = int(count_tasks)

        if (_count_tasks <= 0):
            messagebox.showwarning(
                "Ошибка!",
                "Количество заявок --- целое неотрицательное число"
            )
            return

        return _count_tasks

    def __get_repeat_percent(self):
        """
        Метод позволяет получить процент заявок, что будет возвращены в генератор
        """
        values = self._frame_queue_system_params.get_values()
        repeat_percent = values["Процент возврата"]

        if not self.__is_number(repeat_percent):
            messagebox.showwarning(
                "Ошибка!",
                "Необходимо ввести число --- процент заявок, что будут обработаны повторно"
            )
            return

        _repeat_percent = 0

        if checks.check_int(repeat_percent):
            _repeat_percent = int(repeat_percent)
        else:
            _repeat_percent = float(repeat_percent)

        if (_repeat_percent < 0 or _repeat_percent > 100):
            messagebox.showwarning(
                "Ошибка!",
                "Процент возврата --- неотрицательное число от 0 до 100"
            )
            return

        return _repeat_percent

    def __get_queue_system_type(self):
        """
        Метод позволяет получить данные о проценте возвращенных на обработку заявок, если такой тип СМО был выбран
        """
        repeat_percent = None

        queue_system_type = self._var_choose_queue_system_type.get()

        match queue_system_type:
            case self._with_feedback:
                repeat_percent = self.__get_repeat_percent()
            case self._without_feedback:
                pass
            case _:
                messagebox.showwarning(
                    "Ошибка!",
                    "Выбран неизвестный закон распределения!"
                )

        if not repeat_percent:
            repeat_percent = 0

        return repeat_percent

    def __get_delta_t(self):
        """
        Метод получает параметр λ распределения Пуассона
        """
        values = self._frame_time_advance_params.get_values()
        delta_t = values["Δt"]

        if not self.__is_number(delta_t):
            messagebox.showwarning(
                "Ошибка!",
                "Необходимо ввести параметр Δt"
            )
            return

        _delta_t = 0

        if checks.check_int(delta_t):
            _delta_t = int(delta_t)
        else:
            _delta_t = float(delta_t)

        if (_delta_t <= 0):
            messagebox.showwarning(
                "Ошибка!",
                "Δt --- неотрицательное число"
            )
            return

        return _delta_t

    def __simutale_with_event_approach(self):
        """
        Метод для молирования с помощью событийного принципа
        """

        generator = self.__create_generator()
        if not generator:
            return

        server = self.__create_server()
        if not server:
            return

        buffer_memory = BufferMemory()

        count_tasks = self.__get_count_tasks()
        if not count_tasks:
            return

        repeat_percent = self.__get_queue_system_type()

        event_approach = EventApproach(
            generator, buffer_memory, server, count_tasks, repeat_percent
        )

        return event_approach.run()

    def __simutale_with_delta_t_approach(self):
        """
        Метод для молирования с помощью принципа Δt
        """

        generator = self.__create_generator()
        if not generator:
            return

        server = self.__create_server()
        if not server:
            return

        buffer_memory = BufferMemory()

        count_tasks = self.__get_count_tasks()
        if not count_tasks:
            return

        repeat_percent = self.__get_queue_system_type()

        delta_t = self.__get_delta_t()
        if not delta_t:
            return

        delta_t_approach = DeltaTApproach(
            generator, buffer_memory, server, delta_t, count_tasks, repeat_percent
        )

        return delta_t_approach.run()

    def __run_simulation(self):
        """
        Метод для проведения моделирования
        """

        server = None

        time_advance_alg = self._var_choose_time_advance_alg.get()

        queue_len = 0

        match time_advance_alg:
            case self._event_approach:
                queue_len = self.__simutale_with_event_approach()
            case self._delta_t_approach:
                queue_len = self.__simutale_with_delta_t_approach()
            case _:
                messagebox.showwarning(
                    "Ошибка!",
                    "Выбран неизвестный алгоритм протяжки модельного времени!"
                )

        if queue_len is None:
            return

        match time_advance_alg:
            case self._event_approach:
                self._table.create_and_place_table(1, 1, ["Событийный принцип"], [
                                                   "Оптимальная длина очереди"])
            case self._delta_t_approach:
                self._table.create_and_place_table(1, 1, ["Принцип Δt"], [
                                                   "Оптимальная длина очереди"])
            case _:
                messagebox.showwarning(
                    "Ошибка!",
                    "Выбран неизвестный алгоритм протяжки модельного времени!"
                )

        self._table.set_data([[f"{queue_len}"]])

        return server

    def __is_number(self, x: str) -> bool:
        """
        Метод проверка введенного значения на число
        """
        if checks.check_int(x) or checks.check_float(x):
            return True

        return False

    def __get_uniform_a_b(self, frame: DistributionParamsFrame):
        """
        Метод получает параметры a и b равномерного распределения
        """
        values = frame.get_values()
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

        if checks.check_int(b):
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

    def __get_erlang_k_lamb(self, frame: DistributionParamsFrame):
        """
        Метод получает параметры k и λ распределения Эрланга
        """
        values = frame.get_values()
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

    def __get_poisson_lamb(self, frame: DistributionParamsFrame):
        """
        Метод получает параметр λ распределения Пуассона
        """
        values = frame.get_values()
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

    def __get_exponential_lamb(self, frame: DistributionParamsFrame):
        """
        Метод получает параметр λ экспоненциального распределения
        """
        values = frame.get_values()
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

    def __get_normal_mu_sigma(self, frame: DistributionParamsFrame):
        """
        Метод получает параметры μ и σ нормального распределения
        """
        values = frame.get_values()
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

        if checks.check_int(sigma):
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
