import tkinter as tk
from copy import deepcopy
from reportlab.lib.pdfencrypt import padding

import config_display as cfg


class Display(tk.Frame):
    """
    Класс для дисплея, на котором будут отображаться результаты
    """

    def __init__(self, master=None, **kwargs):
        """
        Инициализация атрибутов класса
        """
        super().__init__(master, **kwargs)
        self.cfgDisp = cfg.ConfigDisplay()
        self.grid_anchor("n")
        self.mtr_entries: list[list[tk.Entry]] = list()
        self.list_labels_row: list[tk.Label] = list()
        self.list_labels_col: list[tk.Label] = list()

    def __create_label(self, text: str):
        """
        Метод для создания кнопки
        """
        return tk.Label(
            self,
            text=text,
            font=(self.cfgDisp.FONT, self.cfgDisp.FONT_SIZE, self.cfgDisp.FONT_STYLE),  # default
            background="#D6DBDB",
        )

    def __create_labels_states(self, cnt_states: int):
        """
        Метод, создающий метки для состояний: S_1, S_2, ...
        """
        self.list_labels_row.clear()
        self.list_labels_col.clear()

        for i in range(cnt_states):
            curr_label_row = self.__create_label(f"S_{i + 1}")
            curr_label_col = self.__create_label(f"S_{i + 1}")
            self.list_labels_row.append(curr_label_row)
            self.list_labels_col.append(curr_label_col)

    def __create_matrix_states(self, cnt_states: int):
        """
        Метод, создающий матрицу полей ввода для матрицы интенсивностей перехода состояний
        """
        self.mtr_entries.clear()

        for i in range(cnt_states):
            tmp = list()
            for j in range(cnt_states):
                curr_entry = tk.Entry(
                    self,
                    width=self.cfgDisp.ENTRY_WIDTH,  # default
                    relief=tk.SUNKEN,
                    borderwidth=self.cfgDisp.ENTRY_BORDER_WIDTH,  # default
                    justify=tk.CENTER,
                    font=(self.cfgDisp.FONT, self.cfgDisp.FONT_SIZE, self.cfgDisp.FONT_STYLE),  # default
                )
                tmp.append(curr_entry)

            self.mtr_entries.append(tmp)

    def create_and_place_matrix_states(self, cnt_states: int):
        """
        Метод для создания и размещения матрицы переходов состояний на дисплее
        """
        # cnt_states = 3  # debug
        # tmp = [
        #     [1.01, 2.95, 3.39],
        #     [3.07, 3.71, 3.80],
        #     [3.55, 0.02, 0.83],
        # ]

        self.__create_matrix_states(cnt_states)
        self.__create_labels_states(cnt_states)

        # строчка меток сверху
        for i in range(cnt_states):
            self.list_labels_row[i].grid(row=0, column=i + 1, padx=5, pady=5)
            self.list_labels_row[i].grid_anchor("s")

        for i in range(cnt_states):
            self.list_labels_col[i].grid(row=i + 1, column=0, padx=5, pady=5)
            self.list_labels_col[i].grid_anchor("s")
            for j in range(cnt_states):
                self.mtr_entries[i][j].grid(row=i + 1, column=j + 1, padx=5, pady=5)
                # self.mtr_entries[i][j].insert(0, f"{tmp[i][j]}")  # debug
                self.mtr_entries[i][j].grid_anchor("s")

    def add_result_prob_and_times(self, probs: list[int | float], stable_times: list[int | float]):
        """
        Метод позволяет добавить вычисленные вероятности состояний
        и время стабилизации на дисплей
        """
        lbl_header = self.__create_label("Результаты")
        lbl_header.grid(row=100, column=0, columnspan=len(self.mtr_entries) + 1, padx=5, pady=5)

        lbl_p = self.__create_label("P")
        lbl_p.grid(row=101, column=0, padx=5, pady=5)

        for i in range(len(probs)):
            lbl_p_val = self.__create_label(f"{probs[i]:.3f}")
            lbl_p_val.config(background=self.cfgDisp.WHITE, relief=tk.SUNKEN)
            lbl_p_val.grid(row=101, column=i + 1, padx=5, pady=5)

        lbl_t = self.__create_label("T")
        lbl_t.grid(row=102, column=0, padx=5, pady=5)

        for i in range(len(probs)):
            lbl_t_val = self.__create_label(f"{stable_times[i]:.3f}")
            lbl_t_val.config(background=self.cfgDisp.WHITE, relief=tk.SUNKEN)
            lbl_t_val.grid(row=102, column=i + 1, padx=5, pady=5)

    def clear(self):
        """
        Метод для очистки дисплея
        """
        self.list_labels_row.clear()
        self.list_labels_col.clear()
        self.mtr_entries.clear()

        for widget in self.winfo_children():
            widget.destroy()
