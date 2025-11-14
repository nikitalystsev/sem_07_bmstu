# три типа событий в информационном центре
CLIENT_EVENT = 1
OPERATOR1_EVENT = 2
OPERATOR2_EVENT = 3
OPERATOR3_EVENT = 4
COMPUTER1_EVENT = 5
COMPUTER2_EVENT = 6


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
        Метод возвращает тип события (от клиента, оператора или от компьютера)
        """
        return self._type
