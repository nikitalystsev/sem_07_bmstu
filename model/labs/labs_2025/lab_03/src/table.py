import tkinter as tk

import config_GUI as cfg


class Table(tk.Frame):
    """
    Класс матрицы интенсивности
    """

    def __init__(self, master=None, **kwargs):
        """
        Инициализация атрибутов класса
        """
        super().__init__(master, **kwargs)
        self.grid_anchor("n")
        self.mtr_entries: list[list[tk.Entry]] = list()
        self.list_labels_row: list[tk.Label] = list()
        self.list_labels_col: list[tk.Label] = list()

    def __create_label(self, text: str):
        """
        Метод для создания label
        """
        return tk.Label(
            self,
            text=text,
            font=(cfg.ConfigGUI.FONT, 15, cfg.ConfigGUI.FONT_STYLE),
            background="#b0b0b0",
            width=5
        )

    def __create_headers(self, cnt_rows: int, cnt_cols: int, row_headers: list, col_headers: list):
        """
        Метод, создающий заголовки таблицы
        """
        self.list_labels_row.clear()
        self.list_labels_col.clear()

        for i in range(cnt_rows):
            curr_label_row = self.__create_label(row_headers[i])
            self.list_labels_row.append(curr_label_row)

        for i in range(cnt_cols):
            curr_label_col = self.__create_label(col_headers[i])
            self.list_labels_col.append(curr_label_col)

    def __create_table(self, cnt_rows: int, cnt_cols: int):
        """
        Метод, создающий строки и столбцы таблицы
        """
        self.mtr_entries.clear()

        for _ in range(cnt_rows):
            tmp = list()
            for _ in range(cnt_cols):
                curr_entry = tk.Entry(
                    self,
                    relief=tk.SUNKEN,
                    justify=tk.CENTER,
                    width=5,  # in symbols
                    borderwidth=3,
                    highlightbackground="#b0b0b0",
                    highlightcolor="#b0b0b0",
                    font=(cfg.ConfigGUI.FONT, 15, 'normal')

                )

                tmp.append(curr_entry)

            self.mtr_entries.append(tmp)

    def create_and_place_table(self, cnt_rows: int, cnt_cols: int, row_headers: list, col_headers: list):
        """
        Метод для создания и размещения матрицы переходов состояний на дисплее
        """
        # cnt_states = 3  # debug
        # tmp = [
        #     [1.01, 2.95, 3.39],
        #     [3.07, 3.71, 3.80],
        #     [3.55, 0.02, 0.83],
        # ]

        self.__create_table(cnt_rows, cnt_cols)
        self.__create_headers(cnt_rows, cnt_cols, row_headers, col_headers)

        # строчка меток сверху
        for i in range(cnt_cols):
            self.list_labels_col[i].grid(row=1, column=i + 1, padx=1, pady=1)
            self.list_labels_col[i].grid_anchor("s")

        for i in range(cnt_rows):
            self.list_labels_row[i].grid(
                row=i + 1 + 1, column=0, padx=1, pady=1)
            self.list_labels_row[i].grid_anchor("s")
            for j in range(cnt_cols):
                self.mtr_entries[i][j].grid(
                    row=i + 1 + 1, column=j + 1, padx=1, pady=1)
                # self.mtr_entries[i][j].insert(0, f"{tmp[i][j]}")  # debug
                self.mtr_entries[i][j].grid_anchor("s")

    def set_data(self, data: list[list[str]]):
        """
        Устанавливает данные в таблицу
        """
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                if i < len(self.mtr_entries) and j < len(self.mtr_entries[i]):
                    self.mtr_entries[i][j].delete(0, tk.END)
                    self.mtr_entries[i][j].insert(0, value)
    # def add_result_prob_and_times(self, probs: list[int | float], stable_times: list[int | float]):
    #     """
    #     Метод позволяет добавить вычисленные вероятности состояний
    #     и время стабилизации на дисплей
    #     """
    #     lbl_header = self.__create_label("Результаты")
    #     lbl_header.grid(row=100, column=0, columnspan=len(
    #         self.mtr_entries) + 1, padx=5, pady=5)

    #     lbl_p = self.__create_label("P")
    #     lbl_p.grid(row=101, column=0, padx=5, pady=5)

    #     for i in range(len(probs)):
    #         lbl_p_val = self.__create_label(f"{probs[i]:.3f}")
    #         lbl_p_val.config()
    #         lbl_p_val.grid(row=101, column=i + 1, padx=5, pady=5)

    #     lbl_t = self.__create_label("T")
    #     lbl_t.grid(row=102, column=0, padx=5, pady=5)

    #     for i in range(len(probs)):
    #         lbl_t_val = self.__create_label(f"{stable_times[i]:.3f}")
    #         lbl_t_val.config()
    #         lbl_t_val.grid(row=102, column=i + 1, padx=5, pady=5)

    def clear(self):
        """
        Метод для очистки дисплея
        """
        self.list_labels_row.clear()
        self.list_labels_col.clear()
        self.mtr_entries.clear()

        for widget in self.winfo_children():
            widget.destroy()
