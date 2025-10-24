import tkinter as tk

from config_GUI import ConfigGUI


class DistributionParamsFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parameters = []
        self.entries = {}
        self.widgets = []  # список всех созданных виджетов

    def set_parameters(self, parameters):
        """
        Принимает список кортежей (имя_параметра, описание)
        и вызывает создание интерфейса.
        """
        self.parameters = parameters
        self.create_widgets()

    def create_widgets(self):
        """Создаёт все лейблы и поля ввода на фрейме."""
        self.clear()  # сначала очищаем старые виджеты

        for i, (name) in enumerate(self.parameters):
            label_name = tk.Label(self, text=name, font=(
                ConfigGUI.FONT, 18, ConfigGUI.FONT_STYLE), justify='center', background="#3D517F", foreground=ConfigGUI.WHITE)
            label_name.grid(row=i, column=0, columnspan=2,
                            sticky="wens", padx=10, pady=5)

            entry = tk.Entry(self, font=(
                ConfigGUI.FONT, 18, ConfigGUI.FONT_STYLE), justify='center', borderwidth=3,
                highlightbackground="#b0b0b0",
                highlightcolor="#b0b0b0")
            entry.grid(row=i, column=2, columnspan=2,
                       sticky="wens", padx=10, pady=5)

            # сохраняем ссылки
            self.entries[name] = entry
            self.widgets.extend([label_name, entry])

        self.columnconfigure(1, weight=1)

    def get_values(self):
        """Возвращает словарь {имя_параметра: значение}"""
        return {name: entry.get() for name, entry in self.entries.items()}

    def clear(self):
        """Удаляет все созданные виджеты с фрейма."""
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
        self.entries.clear()


# # Пример использования
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Параметры модели")

#     frame = ParameterFrame(root, bd=2, relief="groove", padx=10, pady=10)
#     frame.pack(padx=10, pady=10, fill="x")

#     params = [
#         ("α", "Коэффициент обучения (learning rate)"),
#         ("β", "Параметр сглаживания"),
#         ("n_iter", "Количество итераций"),
#     ]

#     frame.set_parameters(params)

#     def show_values():
#         print(frame.get_values())

#     def reset():
#         frame.clear()

#     tk.Button(root, text="Показать значения", command=show_values).pack(pady=5)
#     tk.Button(root, text="Очистить", command=reset).pack(pady=5)

#     root.mainloop()
