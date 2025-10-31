
from queue_system_components.event import Event, EventType
from queue_system_components.generator import Generator
from queue_system_components.buffer_memory import BufferMemory
from queue_system_components.server import Server

import random


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
    Класс, реализующий событийный принцип протяжки модельного времени 
    """

    def __init__(
        self,
        generator: Generator,
        buffer_memory: BufferMemory,
        server: Server,
        count_tasks: int,
        repeat_percent: int | float
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self._generator = generator
        self._buffer_memory = buffer_memory
        self._server = server

        self._count_tasks = count_tasks
        self._sbs: SBS = SBS()  # список будущих событий

        # процент заявок, что будут повторно обработаны
        self._repeat_percent = repeat_percent

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

                # некоторый процент заявок снова пойдет на вход
                if random.randint(1, 100) < self._repeat_percent:
                    self._buffer_memory.write_request(curr_event.get_time())

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


class DeltaTApproach:
    """
    Класс, реализующий принцип Δt протяжки модельного времени
    """

    def __init__(
        self,
        generator: Generator,
        buffer_memory: BufferMemory,
        server: Server,
        delta_t: int | float,
        count_tasks: int,
        repeat_percent: int | float,
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self._generator = generator
        self._buffer_memory = buffer_memory
        self._server = server

        self._count_tasks = count_tasks
        self._delta_t = delta_t

        # процент заявок, что будут повторно обработаны
        self._repeat_percent = repeat_percent

        print(f"self._count_tasks = {self._count_tasks}")
        print(f"self._delta_t = {self._delta_t}")
        print(f"self._repeat_percent = {self._repeat_percent}")

    def run(self):
        """
        Метод реализующий принцип Δt
        """
        self._server.set_state("free")
        count_tasks_processed = 0  # сколько заявок обработано

        # время освобождения ОА после обработки первой заявки (пока неизвестно)
        server_time = -1

        # получаем время прихода первой заявки от ИИ
        new_task_time = self._generator.gen_next_task_time()

        curr_time = self._delta_t

        empty_generated = None

        while count_tasks_processed < self._count_tasks:  # пока все заявки не будут обработаны
            # print("[+] loop...")
            # print(f"count_tasks_processed = {count_tasks_processed}")
            if curr_time > new_task_time:  # если текущее время больше чем время появления новой заявки
                if self._server.is_free() and self._buffer_memory.is_empty():
                    empty_generated = True
                # кладем заявку с какими либо данными в буфферную память
                self._buffer_memory.write_request(curr_time)
                # нужно сгенерить время прихода след заявки
                prev_task_time = new_task_time
                new_task_time = prev_task_time + self._generator.gen_next_task_time()

            if 0 < server_time < curr_time:  # если текущее время больше чем время освобождения ОА после обработки очередной заявки
                self._server.set_state("free")  # ОА стал свободным

                # некоторый процент заявок снова пойдет на вход
                if random.randint(0, 100) < self._repeat_percent:
                    self._buffer_memory.write_request(0)

                count_tasks_processed += 1

            if self._server.is_free():  # если ОА свободен
                # пытаемся считать ранее положенную заявку из буферной памяти
                is_empty, _ = self._buffer_memory.read_request()

                if is_empty:  # если буферная память пуста --- положить в ОА нечего
                    server_time = -1
                else:
                    server_time = (prev_task_time if empty_generated else server_time) + \
                        self._server.get_process_task_time()

                    # ОА обрабатывает заявку
                    self._server.set_state("busy")

            empty_generated = False
            curr_time += self._delta_t  # продвигаем модельное время

        return self._buffer_memory.get_max_queue_len()
