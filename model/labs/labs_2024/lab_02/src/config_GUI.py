from dataclasses import dataclass


@dataclass
class ConfigGUI:
    """
    Класс конфигурации параметров экрана
    """

    FRAME_WIDGET_WIDTH = 400 # в пикселях
    FONT = "helvetica"
    FONT_SIZE = 14
    FONT_STYLE = 'bold'

    # entry
    ENTRY_BORDER_WIDTH = 3 # в пикселях
    ENTRY_WIDTH = 15 # в символах

    # colors
    BLACK = "#000000"
    WHITE = "#FFFFFF"
    ORANGE = "#FFA500"
    RED = "#FF0000"
    DARKCYAN = "DarkCyan"
    GREEN = "#008000"
    BLUE = "#0000FF"
    VIOLET = "#800080"
    YELLOW = "#FFFF00"
    Aquamarine = "#7FFFD4"
    LightCyan = "#E0FFFF"
    SILVER = "#C0C0C0"
    SteelBlue = "#4682B4"
