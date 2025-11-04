SERVER_EVENT = 1
GENERATOR_EVENT = 2


class Event:
    """
    Класс, представляющий собой событие в СМО
    """

    def __init__(self, time: float, _type: int):
        """
        Инициализация атрибутов класса
        """
        self._time = time
        self._type = _type

    def get_time(self):
        """
        Метод возвращает время наступления события
        """
        return self._time

    def get_type(self):
        """
        Метод возвращает тип события (от генератора ли от ОА)
        """
        return self._type
