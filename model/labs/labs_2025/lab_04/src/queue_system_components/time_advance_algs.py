
from queue_system_components.event import Event, SERVER_EVENT, GENERATOR_EVENT
from queue_system_components.generator import Generator
from queue_system_components.buffer_memory import BufferMemory
from queue_system_components.server import Server

import random


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
        generator: Generator,  # генератор
        buffer_memory: BufferMemory,  # буфферная память
        server: Server,  # обслуживающий аппарат
        count_tasks: int,
        repeat_percent: int | float
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self._generator = generator
        self._buffer_memory = buffer_memory
        self._server = server

        self._count_tasks = count_tasks  # число заявок, которые нужно промоделировать
        self._sbs: SBS = SBS()  # список будущих событий

        # процент заявок, что будут повторно обработаны
        self._repeat_percent = repeat_percent

    def __prepare(self):
        """
        Подготовительные операции перед началом моделирования
        """
        self._sbs.clean()  # очищаем список будущих событий

        # генератор свободен (моделирование еще не началось)
        self._server.set_state("free")

        start_generator_event = Event(  # событие --- момент появления первой заявки (сообщения) от генератора (t11)
            self._generator.gen_next_task_time(), GENERATOR_EVENT
        )
        self._sbs.add_event(start_generator_event)

    def run(self):
        """
        Метод реализующий событийный принцип
        """

        count_tasks_processed = 0  # число обработанных ОА-м заявок

        self.__prepare()  # выполняем подготовительные действия

        while count_tasks_processed < self._count_tasks:  # пока все заявки не будут обработаны
            # print(f"count_tasks_processed = {count_tasks_processed}")
            # берется минимальное из списка будущих событий
            curr_event = self._sbs.get_event()

            if curr_event.get_type() == GENERATOR_EVENT:  # появилось сообщение от генератора
                # реализуем событие --- записали его в буферную память и с пом. генератора получили момент след сообщения
                self._buffer_memory.write_request(  # кладем его в буферную память
                    curr_event.get_time()
                )
                next_event = Event(
                    # продвигаем модельное время
                    curr_event.get_time() + self._generator.gen_next_task_time(), GENERATOR_EVENT
                )
                # помещаем новое событие в список будущих событий
                self._sbs.add_event(next_event)

            if curr_event.get_type() == SERVER_EVENT:  # ОА обработал заявку, то есть освободился
                # устанавливаем флаг что свободен
                self._server.set_state("free")

                # некоторый процент заявок снова пойдет на вход
                if random.randint(1, 100) < self._repeat_percent:
                    self._buffer_memory.write_request(curr_event.get_time())
                else:
                    count_tasks_processed += 1  # заявка была обработана

            if self._server.is_free():  # если ОА свободен
                # пытаемся считать ранее положенную заявку из буферной памяти
                is_empty, _ = self._buffer_memory.read_request()

                if not is_empty:  # если буферная память пуста --- положить в ОА нечего
                    next_event = Event(
                        # продвигаем модельное время
                        curr_event.get_time() + self._server.get_server_task_time(), SERVER_EVENT
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
        generator: Generator,  # генератор
        buffer_memory: BufferMemory,  # буфферная память
        server: Server,  # обслуживающий аппарат
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

    def run(self):
        """
        Метод реализующий принцип Δt
        """
        self._server.set_state("free")
        count_tasks_processed = 0  # сколько заявок обработано

        # получаем время прихода первой заявки от генератора
        new_task_time = self._generator.gen_next_task_time()
        prev_task_time = 0

        server_task_time = -1

        curr_time = self._delta_t  # время t + Δt

        all_empty = None

        while count_tasks_processed < self._count_tasks:  # пока все заявки не будут обработаны
            # последовательный анализ каждого блока системы в момент времени t + Δt (curr_time)
            # по заданному состоянию блоков в момент времени t

            # анализ генератора
            # проверяем в цикле, т.к. за один шаг Δt может прийти несколько заявок
            if curr_time > new_task_time:
                if self._server.is_free() and self._buffer_memory.is_empty():  # если система пустая
                    all_empty = True
                # заявка должна быть в буферной памяти
                self._buffer_memory.write_request(new_task_time)
                # нужно сгенерить время прихода след заявки
                prev_task_time = new_task_time
                new_task_time = prev_task_time + self._generator.gen_next_task_time()

            # анализ ОА
            # если текущее время больше чем время освобождения ОА после обработки очередной заявки
            if curr_time > server_task_time and server_task_time > 0:
                self._server.set_state("free")  # ОА должен быть свободным

                # некоторый процент заявок снова пойдет на вход
                if random.randint(0, 100) < self._repeat_percent:
                    self._buffer_memory.write_request(0)
                else:
                    count_tasks_processed += 1
            else:  # ниче не делаем
                pass

            if self._server.is_free():  # если ОА свободен
                # должны пытаться считать ранее положенную заявку из буферной памяти
                is_empty, _ = self._buffer_memory.read_request()

                if not is_empty:  # если буферная память пуста --- положить в ОА нечего
                    duration = self._server.get_server_task_time()

                    # если ОА был занят, то в момент когда он стал свободен и есть новая заявка на обработку,
                    # протяжка модельного времени обслуживания идет исходя из предыдущего времени освобождения ОА
                    # если ОА был свободен, то он и сейчас свободен и есть новая заявка на обработку,
                    # протяжка модельного времени обслуживания идет исходя из времени поступления заявки в буферную память (очередь)
                    started_time = prev_task_time if all_empty else server_task_time
                    server_task_time = started_time + duration

                    # ОА обрабатывает заявку
                    self._server.set_state("busy")
                else:
                    server_task_time = -1

            all_empty = False
            curr_time += self._delta_t  # продвигаем модельное время

        return self._buffer_memory.get_max_queue_len()
