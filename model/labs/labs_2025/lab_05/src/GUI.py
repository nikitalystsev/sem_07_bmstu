
from tkinter import messagebox
import tkinter as tk

import config_GUI as cfg

from interval_params_frame import IntervalParamsFrame

from queue_system_components.distributions import UniformDistribution
from queue_system_components.event_approach import EventApproach
from queue_system_components.client import Client
from queue_system_components.buffer_memory import BufferMemory
from queue_system_components.computer import Computer
from queue_system_components.my_operator import Operator

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

        self.title("Лабораторная №5, Лысцев Никита ИУ7-73Б")

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
        self._frame_widgets.pack(side=tk.LEFT, fill="both")

        self._frame_results = self.__create_frame(master=self)
        self._frame_results.config(background="#b0b0b0")
        self._frame_results.pack(side=tk.LEFT, expand=True, fill="both")

        # # widgets
        # # -----------------------------------------------

        self._lbl_center = self.__create_label(
            master=self._frame_widgets, text="Информационный центр"
        )
        self._lbl_center.config(
            font=(self.cfgWin.FONT, 25, self.cfgWin.FONT_STYLE), background="#3D517F"
        )
        self._lbl_center.grid(
            row=0, column=0, columnspan=4, padx=10, pady=15
        )

        self._lbl_clients = self.__create_label(
            master=self._frame_widgets, text="Клиенты"
        )
        self._lbl_clients.config(
            font=(self.cfgWin.FONT, 21, self.cfgWin.FONT_STYLE), background="#3D517F"
        )
        self._lbl_clients.grid(
            row=1, column=0, columnspan=4, sticky='wens', padx=10, pady=5
        )

        self._lbl_client = self.__create_label(
            master=self._frame_widgets, text="Интервал прихода клиентов"
        )
        self._lbl_client.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE), background="#3D517F",
            anchor="w"
        )
        self._lbl_client.grid(
            row=2, column=0, columnspan=4, sticky='wens', padx=10
        )

        self._client_interval = IntervalParamsFrame(parent=self._frame_widgets)
        self._client_interval.create_widgets()
        self._client_interval.set_data(data=[10, 2])
        self._client_interval.grid(
            row=3, column=0, columnspan=4, sticky="wens", padx=10, pady=15
        )

        self._lbl_operators = self.__create_label(
            master=self._frame_widgets, text="Операторы"
        )
        self._lbl_operators.config(
            font=(self.cfgWin.FONT, 21, self.cfgWin.FONT_STYLE), background="#3D517F"
        )
        self._lbl_operators.grid(
            row=4, column=0, columnspan=4, sticky='wens', padx=10, pady=5
        )

        self._lbl_operator1 = self.__create_label(
            master=self._frame_widgets, text="Время обслуживания оператора 1"
        )
        self._lbl_operator1.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE), background="#3D517F",
            anchor="w"
        )
        self._lbl_operator1.grid(
            row=5, column=0, columnspan=4, sticky='wens', padx=10
        )

        self._operator1_interval = IntervalParamsFrame(
            parent=self._frame_widgets)
        self._operator1_interval.create_widgets()
        self._operator1_interval.set_data(data=[20, 5])
        self._operator1_interval.grid(
            row=6, column=0, columnspan=4, sticky="wens", padx=10, pady=15
        )

        self._lbl_operator2 = self.__create_label(
            master=self._frame_widgets, text="Время обслуживания оператора 2"
        )
        self._lbl_operator2.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE), background="#3D517F",
            anchor="w"
        )
        self._lbl_operator2.grid(
            row=7, column=0, columnspan=4, sticky='wens', padx=10
        )

        self._operator2_interval = IntervalParamsFrame(
            parent=self._frame_widgets)
        self._operator2_interval.create_widgets()
        self._operator2_interval.set_data(data=[40, 10])
        self._operator2_interval.grid(
            row=8, column=0, columnspan=4, sticky="wens", padx=10, pady=15)

        self._lbl_operator3 = self.__create_label(
            master=self._frame_widgets, text="Время обслуживания оператора 3"
        )
        self._lbl_operator3.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE), background="#3D517F",
            anchor="w"
        )
        self._lbl_operator3.grid(
            row=9, column=0, columnspan=4, sticky='wens', padx=10
        )

        self._operator3_interval = IntervalParamsFrame(
            parent=self._frame_widgets)
        self._operator3_interval.create_widgets()
        self._operator3_interval.set_data(data=[40, 20])
        self._operator3_interval.grid(
            row=10, column=0, columnspan=4, sticky="wens", padx=10, pady=15
        )

        self._lbl_computers = self.__create_label(
            master=self._frame_widgets, text="Компьютеры"
        )
        self._lbl_computers.config(
            font=(self.cfgWin.FONT, 21, self.cfgWin.FONT_STYLE), background="#3D517F"
        )
        self._lbl_computers.grid(
            row=11, column=0, columnspan=4, sticky='wens', padx=10, pady=5
        )

        self._lbl_computer1 = self.__create_label(
            master=self._frame_widgets, text="Время обработки компьютера 1"
        )
        self._lbl_computer1.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE), background="#3D517F",
            anchor="w"
        )
        self._lbl_computer1.grid(
            row=12, column=0, sticky='wens', padx=10, pady=15
        )

        self._entry_computer1 = self.__create_entry(master=self._frame_widgets)
        self._entry_computer1.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE)
        )
        self._entry_computer1.insert(0, f"{15}")
        self._entry_computer1.grid(
            row=12, column=1, columnspan=2, sticky='wens', padx=10, pady=15
        )

        self._lbl_computer1_minutes = self.__create_label(
            master=self._frame_widgets, text="минут"
        )
        self._lbl_computer1_minutes.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE), background="#3D517F",
            anchor="w"
        )
        self._lbl_computer1_minutes.grid(
            row=12, column=3, sticky='wens', padx=10, pady=15
        )

        self._lbl_computer2 = self.__create_label(
            master=self._frame_widgets, text="Время обработки компьютера 2"
        )
        self._lbl_computer2.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE), background="#3D517F",
            anchor="w"
        )
        self._lbl_computer2.grid(
            row=13, column=0, sticky='wens', padx=10, pady=5
        )

        self._entry_computer2 = self.__create_entry(master=self._frame_widgets)
        self._entry_computer2.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE)
        )
        self._entry_computer2.insert(0, f"{30}")
        self._entry_computer2.grid(
            row=13, column=1, columnspan=2, sticky='wens', padx=10, pady=5
        )

        self._lbl_computer2_minutes = self.__create_label(
            master=self._frame_widgets, text="минут"
        )
        self._lbl_computer2_minutes.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE), background="#3D517F",
            anchor="w"
        )
        self._lbl_computer2_minutes.grid(
            row=13, column=3, sticky='wens', padx=10, pady=5
        )

        self._lbl_computers = self.__create_label(
            master=self._frame_widgets, text="Запросы"
        )
        self._lbl_computers.config(
            font=(self.cfgWin.FONT, 21, self.cfgWin.FONT_STYLE), background="#3D517F"
        )
        self._lbl_computers.grid(
            row=14, column=0, columnspan=4, sticky='wens', padx=10, pady=10
        )

        self._lbl_count_tasks = self.__create_label(
            master=self._frame_widgets, text="Количество запросов"
        )
        self._lbl_count_tasks.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE), background="#3D517F",
        )
        self._lbl_count_tasks.grid(
            row=15, column=0, sticky='wens', padx=10, pady=10
        )

        self._entry_count_tasks = self.__create_entry(
            master=self._frame_widgets
        )
        self._entry_count_tasks.config(
            font=(self.cfgWin.FONT, 18, self.cfgWin.FONT_STYLE)
        )
        self._entry_count_tasks.insert(0, f"{300}")
        self._entry_count_tasks.grid(
            row=15, column=1, columnspan=3, sticky='wens', padx=10, pady=10
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
            row=18, column=0, columnspan=4,
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

    def __create_client(self):
        """
        Метод создает клиента
        """
        params = self.__get_interval(
            self._client_interval
        )
        if params is None:
            messagebox.showwarning(
                "Ошибка!",
                "Клиент для генерации запросов не был успешно создан!"
            )
            return

        a = params[0] - params[1]
        b = params[0] + params[1]

        print(f"creating client: a = {a}, b = {b}")

        return Client(UniformDistribution(a, b))

    def __create_operator(self, frame: IntervalParamsFrame, num: int):
        """
        Метод создает оператора
        """
        params = self.__get_interval(
            frame=frame
        )
        if params is None:
            messagebox.showwarning(
                "Ошибка!",
                f"Оператор {num} для обслуживания запросов не был успешно создан!"
            )
            return

        a = params[0] - params[1]
        b = params[0] + params[1]

        print(f"creating operator {num}: a = {a}, b = {b}")

        return Operator(UniformDistribution(a, b))

    def _create_operators(self):
        """
        Метод создает всех операторов
        """

        operator1 = self.__create_operator(
            frame=self._operator1_interval,
            num=1
        )
        if not operator1:
            return

        operator2 = self.__create_operator(
            frame=self._operator2_interval,
            num=2
        )
        if not operator2:
            return

        operator3 = self.__create_operator(
            frame=self._operator3_interval,
            num=3
        )
        if not operator3:
            return

        return operator1, operator2, operator3

    def __create_computer(self, entry: tk.Entry, num: int):
        """
        Метод создает компьютер
        """
        t = self.__get_t(
            entry=entry
        )
        if t is None:
            messagebox.showwarning(
                "Ошибка!",
                f"Компьютер {num} для обработки запросов не был успешно создан!"
            )
            return

        print(f"creating computer {num}: t = {t}")

        return Computer(t)

    def _create_computers(self):
        """
        Метод создает все компьютеры
        """

        computer1 = self.__create_computer(
            entry=self._entry_computer1,
            num=1
        )
        if not computer1:
            return

        computer2 = self.__create_computer(
            entry=self._entry_computer2,
            num=2
        )
        if not computer2:
            return

        return computer1, computer2

    def __get_count_tasks(self):
        """
        Метод позволяет получить необходимое для обслуживания количество заявок
        """
        count_tasks = self._entry_count_tasks.get()

        if not self.__is_number(count_tasks):
            messagebox.showwarning(
                "Ошибка!",
                "Необходимо ввести целое число --- количество запросов на обработку"
            )
            return

        _count_tasks = 0

        if checks.check_int(count_tasks):
            _count_tasks = int(count_tasks)

        if (_count_tasks <= 0):
            messagebox.showwarning(
                "Ошибка!",
                "Количество запросов --- целое положительное число"
            )
            return

        print(f"count_tasks = {count_tasks}")

        return _count_tasks

    def __get_t(self, entry: tk.Entry):
        """
        Метод получает константное время обрабоки запроса компьютером
        """
        t = entry.get()

        if not self.__is_number(t):
            messagebox.showwarning(
                "Ошибка!",
                "Необходимо ввести число --- врем обработки запроса"
            )
            return

        _t = 0

        if checks.check_int(t):
            _t = int(t)
        else:
            _t = float(t)

        if (_t <= 0):
            messagebox.showwarning(
                "Ошибка!",
                "Время обработки запроса --- положительное число"
            )
            return

        return _t

    def __simutale_with_event_approach(self):
        """
        Метод для молирования с помощью событийного принципа
        """

        client = self.__create_client()
        if not client:
            return

        operators = self._create_operators()
        if not operators:
            return

        computers = self._create_computers()
        if not computers:
            return

        count_tasks = self.__get_count_tasks()
        if not count_tasks:
            return

        event_approach = EventApproach(
            client=client,
            buffer_memory1=BufferMemory(),
            buffer_memory2=BufferMemory(),
            computer1=computers[0],
            computer2=computers[1],
            operator1=operators[0],
            operator2=operators[1],
            operator3=operators[2],
            count_tasks=count_tasks
        )

        return event_approach.run()

    def __run_simulation(self):
        """
        Метод для проведения моделирования
        """

        data = self.__simutale_with_event_approach()
        if not data:
            return

        self._table.create_and_place_table(1, 4, [""], [
            "Отказано", "Обслужено", "Общее число запросов", "Вероятность отказа"])

        data = [[f"{data[0]}", f"{data[1]}", f"{data[2]}", f"{data[3]: .3f}"]]

        self._table.set_data(data=data)

    def __is_number(self, x: str) -> bool:
        """
        Метод проверка введенного значения на число
        """
        if checks.check_int(x) or checks.check_float(x):
            return True

        return False

    def __get_interval(self, frame: IntervalParamsFrame):
        """
        Метод получает значения интервала
        """
        values = frame.get_data()
        if not values:
            return

        val1, val2 = values

        if not self.__is_number(val1) or not self.__is_number(val2):
            messagebox.showwarning(
                "Ошибка!",
                "Необходимо ввести значения интервала"
            )
            return

        _val1, _val2 = 0, 0

        if checks.check_int(val1):
            _val1 = int(val1)
        else:
            _val1 = float(val1)

        if checks.check_int(val2):
            _val2 = int(val2)
        else:
            _val2 = float(val2)

        if (_val1 < 0 or _val2 < 0):
            messagebox.showwarning(
                "Ошибка!",
                "Значения интервала должны быть больше 0"
            )
            return

        return _val1, _val2
