import tkinter as tk


class Table(tk.Frame):
    def __init__(
        self,
        master: tk.Tk | tk.Frame,
        cnt_rows: int,
        cnt_cols: int,
        entries_state,
        headers
    ):
        super().__init__(master=master)
        
        # В __init__ добавь поле-замок:
        self._nav_pressed = set()

        self.cnt_rows = cnt_rows
        self.cnt_cols = cnt_cols
        self.entries: list[list[tk.Entry]] = []
        self.headers = headers
        self.entries_state = entries_state

        
        for j, header in enumerate(self.headers):
            label = tk.Label(self, text=header, width=14)
            label.grid(row=0, column=j, sticky="nsew")

        for i in range(1, cnt_rows + 1):
            row_entries: list[tk.Entry] = []

            for j in range(cnt_cols):
                entry = tk.Entry(
                    self, width=14,
                    state=self.entries_state,
                    disabledbackground='#FFFFFF',
                    disabledforeground='black',
                    readonlybackground='#FFFFFF',
                )
                entry.grid(row=i, column=j)
                row_entries.append(entry)
                self._bind_navigation(entry, i, j)  # ← биндим навигацию
                
            self.entries.append(row_entries)

    def get_data(self):
        """
        Возвращает данные таблицы в виде списка списков
        """
        
        return [[entry.get() for entry in row] for row in self.entries]

    def set_data(self, data: list[list[str]]):
        """
        Устанавливает данные в таблицу
        """
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                if i < len(self.entries) and j < len(self.entries[i]):
                    self.entries[i][j].config(state="normal")
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, value)
                    self.entries[i][j].config(state=self.entries_state)

    def clear(self):
        """
        Очищает все ячейки
        """
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)

    def set_headers(self, headers):
        """
        Устанавливает заголовки столбцов
        """
        for j, header in enumerate(headers):
            label = tk.Label(self, text=header, width=14)
            label.grid(row=0, column=j, sticky="nsew")
            

    def _bind_navigation(self, entry: tk.Entry, i: int, j: int):
        # ВНИЗ: Enter
        entry.bind("<Return>", lambda e, r=i, c=j: self._on_return_down(r, c))
        entry.bind("<Down>", lambda e, r=i, c=j: self._on_return_down(r, c))
        # entry.bind("<Up>", lambda e, r=i, c=j: self._on_return_up(r, c))

    def _on_return_down(self, i, j):
        # Явно вернуть "break", чтобы не всплывало дальше
        self._move_down(i, j)
        return "break"
    
    def focus_cell(self, i: int, j: int):
        i %= self.cnt_rows
        j %= self.cnt_cols
        cell = self.entries[i][j]
        try:
            cell.focus_set()
            cell.icursor(tk.END)
        except tk.TclError:
            pass
        # return "break"

    def _move_down(self, i, j):
        # Исправлено: реально идём на следующую строку
        return self.focus_cell(i % self.cnt_rows, j)


