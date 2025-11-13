from queue_system_components.client import Client
from queue_system_components.buffer_memory import BufferMemory
from queue_system_components.computer import Computer
from queue_system_components.operator import Operator
from queue_system_components.event import Event


class SBS:
    """
    Класс, реализующий список будущих событий 
    """

    def __init__(self) -> None:
        """
        Инициализация атрибутов класса
        """

        self._sbs: list[Event] = list()  # собственно список будущих событий

    def add_event(self, event: Event):
        """
        Метод позволяет добавить событие в список будущих событий
        """
        self._sbs.append(event)
        self._sbs.sort(key=lambda e: e.get_time())

    def get_event(self):
        """
        Вытаскивает событие с минимальным временем из списка будущих событий
        """

        return self._sbs.pop(0)

    def clean(self):
        """
        Метод очищает список будущих событий
        """
        self._sbs.clear()


class EventApproach:
    """
    Класс, реализующий событийный принцип протяжки модельного времени 
    """

    def __init__(
        self,
        client: Client,  # генератор
        buffer_memory1: BufferMemory,  # накопитель 1
        buffer_memory2: BufferMemory,  # накопитель 2
        computer1: Computer,  # компьютер 1
        computer2: Computer,  # компьютер 2
        operator1: Operator,  # оператор 1
        operator2: Operator,  # оператор 2
        operator3: Operator,  # оператор 3
        count_tasks: int,
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self._client = client

        self._buffer_memory1 = buffer_memory1
        self._buffer_memory2 = buffer_memory2

        self._computer1 = computer1
        self._computer2 = computer2

        self._operator1 = operator1
        self._operator2 = operator2
        self._operator3 = operator3

        self._count_tasks = count_tasks

    def run(self):
        """
        Метод реализующий событийный принцип
        """

        count_tasks_processed = 0
        
        while count_tasks_processed < self._count_tasks:
            