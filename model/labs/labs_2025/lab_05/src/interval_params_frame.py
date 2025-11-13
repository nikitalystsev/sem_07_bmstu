import tkinter as tk

from config_GUI import ConfigGUI


class IntervalParamsFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._widgets = []  # список всех созданных виджетов

    def create_widgets(self):
        """
        Создаёт все лейблы и поля ввода на фрейме.
        """
        self.clear()  # сначала очищаем старые виджеты

        entry_interval1 = tk.Entry(master=self)
        entry_interval1.config(
            font=(ConfigGUI.FONT, 18, ConfigGUI.FONT_STYLE),
            borderwidth=3,
            highlightbackground="#b0b0b0",
            highlightcolor="#b0b0b0"
        )
        entry_interval1.pack(side=tk.LEFT)

        lbl_plus_minus = tk.Label(master=self, text="±")
        lbl_plus_minus.config(
            background="#3D517F",
            font=(ConfigGUI.FONT, 18, ConfigGUI.FONT_STYLE),
            foreground=ConfigGUI.WHITE
        )
        lbl_plus_minus.pack(side=tk.LEFT, fill="both", expand=True)

        entry_interval2 = tk.Entry(master=self)
        entry_interval2.config(
            font=(ConfigGUI.FONT, 18, ConfigGUI.FONT_STYLE),
            borderwidth=3,
            highlightbackground="#b0b0b0",
            highlightcolor="#b0b0b0",
        )
        entry_interval2.pack(side=tk.LEFT)

        lbl_minutes = tk.Label(master=self, text="минут")
        lbl_minutes.config(
            background="#3D517F",
            font=(ConfigGUI.FONT, 18, ConfigGUI.FONT_STYLE),
            foreground=ConfigGUI.WHITE
        )
        lbl_minutes.pack(side=tk.LEFT, fill="both", expand=True)

        self._widgets.extend(
            [entry_interval1, lbl_plus_minus, entry_interval2, lbl_minutes]
        )

    def clear(self):
        """
        Удаляет все созданные виджеты с фрейма
        """
        for widget in self._widgets:
            widget.destroy()
        self._widgets.clear()
