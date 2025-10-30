
from event import Event, EventType
from generator import Generator
from buffer_memory import BufferMemory
from server import Server


class SBS:
    """
    Класс, реализующий список будущих событий 
    """

    def __init__(self) -> None:
        self._sbs: list[Event] = list()

    def add_event(self, event: Event):
        """
        Метод позволяет добавить событие в список будущих событий
        """
        self._sbs.append(event)
        self._sbs.sort(key=lambda e: e.get_time())

    def get_event(self):
        """
        Вытаскивает событие с милимальным временем из списка будущих событий
        """

        return self._sbs.pop(0)


class EventApproach:
    """
    Класс, реализующий событийныный принцип протяжки модельного времени 
    """

    def __init__(
        self,
        generator: Generator,
        buffer_memory: BufferMemory,
        server: Server,
        count_tasks: int
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self._generator = generator
        self._buffer_memory = buffer_memory
        self._server = server

        self._count_tasks = count_tasks
        self._sbs: SBS = SBS()  # список будущих событий

    def run(self):
        """
        Метод реализующий событийный принцип
        """
        count_tasks_processed = 0  # сколько заявок обработано

        start_event = Event(
            self._generator.gen_next_task_time(), EventType.GENERATOR
        )
        self._sbs.add_event(start_event)

        while count_tasks_processed < self._count_tasks:  # пока все заявки не будут обработаны
            # берется минимальное из списка будущих событий
            curr_event = self._sbs.get_event()

            if curr_event.get_event_type() == EventType.GENERATOR:  # появилось сообщение от генератора
                self._buffer_memory.write_request(  # кладем его в буферную память
                    curr_event.get_time()
                )
                # реализуем событие --- записали его в буферную память (выше) и с пом. генератора получили момент след сообщения
                next_event = Event(
                    # продвигаем модельное время
                    curr_event.get_time() + self._generator.gen_next_task_time(), EventType.GENERATOR
                )
                # помещаем новое событие в список будущих событий
                self._sbs.add_event(next_event)

            if curr_event.get_event_type() == EventType.SERVER:  # ОА обработал заявку, то есть освободился
                # устанавливаем флаг что свободен
                self._server.set_state("free")

                count_tasks_processed += 1  # заявка была обработана

            if self._server.is_free():  # если ОА свободен
                # пытаемся считать ранее положенную заявку из буферной памяти
                is_empty, _ = self._buffer_memory.read_request()

                if is_empty:  # если буферная память пуста --- положить в ОА нечего
                    pass
                else:
                    next_event = Event(
                        # продвигаем модельное время
                        curr_event.get_time() + self._server.get_process_task_time(), EventType.SERVER
                    )
                    # кладем заявку из буферной памяти в ОА
                    self._sbs.add_event(next_event)
                    self._server.set_state("busy")  # ОА обрабатывает заявку

        return self._buffer_memory.get_max_queue_len()
