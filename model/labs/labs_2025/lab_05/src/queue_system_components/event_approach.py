from queue_system_components.client import Client
from queue_system_components.buffer_memory import BufferMemory
from queue_system_components.computer import Computer
from queue_system_components.my_operator import Operator
from queue_system_components.event import Event, CLIENT_EVENT, OPERATOR1_EVENT, OPERATOR2_EVENT, OPERATOR3_EVENT, COMPUTER1_EVENT, COMPUTER2_EVENT


from queue_system_components.distributions import UniformDistribution, ErlangDistribution, PoissonDistribution, ExponentialDistribution, NormalDistribution


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

    def length(self):
        """
        Мето возвращает длину списка будущих событий
        """

        return len(self._sbs)


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

        # сколько заявок должно быть обработано компьютерами
        self._count_tasks = count_tasks

        self._sbs: SBS = SBS()  # список будущих событий

    def __prepare(self):
        """
        Подготовительные операции перед началом моделирования
        """
        self._sbs.clean()  # очищаем список будущих событий

        # все операторы свободны (моделирование еще не началось)
        self._operator1.set_state("free")
        self._operator2.set_state("free")
        self._operator3.set_state("free")

        # все операторы свободны (моделирование еще не началось)
        self._computer1.set_state("free")
        self._computer2.set_state("free")

        # событие --- момент появления первого запроса от клиента (t11)
        start_client_event = Event(
            self._client.gen_next_task_time(), CLIENT_EVENT
        )
        self._sbs.add_event(start_client_event)

    def run(self):
        """
        Метод реализующий событийный принцип
        """
        self.__prepare()

        count_tasks_processed = 0  # сколько было оработано компьютерами

        count_tasks_refused = 0  # скольким заявкам было отказало в обслуживании

        total_count_tasks = 0
        while count_tasks_processed < self._count_tasks:
            # берется минимальное из списка будущих событий
            # print("loop...")

            curr_event = self._sbs.get_event()

            # print(
            #     f"curr_event.get_type() = {curr_event.get_type() == CLIENT_EVENT}, длина СБС = {self._sbs.length()}"
            # )

            if curr_event.get_type() == CLIENT_EVENT:  # появился новый запрос от клиента
                # нужно посмотреть, какие операторы не заняты и отдать первому свободному
                if self._operator1.is_free():  # первый свободен --- отдаем ему
                    # что значит отдать оператору? мне каж это так:
                    self._operator1.set_state("busy")
                    next_operator_event = Event(
                        curr_event.get_time() + self._operator1.get_operator_task_time(), OPERATOR1_EVENT
                    )
                    self._sbs.add_event(next_operator_event)
                elif self._operator2.is_free():  # второй свободен --- отдаем ему
                    self._operator2.set_state("busy")
                    next_operator_event = Event(
                        curr_event.get_time() + self._operator2.get_operator_task_time(), OPERATOR2_EVENT
                    )
                    self._sbs.add_event(next_operator_event)
                elif self._operator3.is_free():  # третий свободен --- отдаем ему
                    self._operator3.set_state("busy")
                    next_operator_event = Event(
                        curr_event.get_time() + self._operator3.get_operator_task_time(), OPERATOR3_EVENT
                    )
                    self._sbs.add_event(next_operator_event)
                else:
                    count_tasks_refused += 1
                    total_count_tasks += 1

                next_client_event = Event(
                    curr_event.get_time() + self._client.gen_next_task_time(), CLIENT_EVENT
                )
                self._sbs.add_event(next_client_event)

            if curr_event.get_type() == OPERATOR1_EVENT:  # оператор 1 обслужил заявку
                # это значит, что он теперь свободен, нужно положить запрос в накопитель
                # print(
                #     f"operator 1 state = {"free" if self._operator1.is_free() else "busy"}"
                # )
                self._operator1.set_state("free")
                self._buffer_memory1.write_request(curr_event.get_time())

            if curr_event.get_type() == OPERATOR2_EVENT:  # оператор 2 обслужил заявку
                # print(
                #     f"operator 2 state = {"free" if self._operator2.is_free() else "busy"}"
                # )
                self._operator2.set_state("free")
                self._buffer_memory1.write_request(curr_event.get_time())

            if curr_event.get_type() == OPERATOR3_EVENT:  # оператор 3 обслужил заявку
                # print(
                #     f"operator 3 state = {"free" if self._operator3.is_free() else "busy"}"
                # )
                self._operator3.set_state("free")
                self._buffer_memory2.write_request(curr_event.get_time())

            if curr_event.get_type() == COMPUTER1_EVENT:  # компьютер 1 обработал заявку
                # это значит запрос был обработан (увеличиваем счетчик), компьютер теперь свободен
                # print(
                #     f"computer 1 state = {"free" if self._computer1.is_free() else "busy"}"
                # )
                self._computer1.set_state("free")

                count_tasks_processed += 1
                total_count_tasks += 1

            if curr_event.get_type() == COMPUTER1_EVENT:  # компьютер 2 обработал заявку
                self._computer2.set_state("free")

                count_tasks_processed += 1
                total_count_tasks += 1

            if self._computer1.is_free():  # если компьютер 1 свободен
                # пытаемся считать ранее положенную заявку из буферной памяти
                is_empty, _ = self._buffer_memory1.read_request()

                if not is_empty:  # если буферная память пуста --- положить в компьютер 1 нечего
                    next_event = Event(
                        # продвигаем модельное время
                        curr_event.get_time() + self._computer1.t_i(), COMPUTER1_EVENT
                    )
                    # кладем заявку из буферной памяти в компьютер 1
                    self._sbs.add_event(next_event)
                    # компьютер 1 обрабатывает заявку
                    self._computer1.set_state("busy")

            if self._computer2.is_free():  # если компьютер 2 свободен
                # пытаемся считать ранее положенную заявку из буферной памяти
                is_empty, _ = self._buffer_memory2.read_request()

                if not is_empty:  # если буферная память пуста --- положить в компьютер 2 нечего
                    next_event = Event(
                        # продвигаем модельное время
                        curr_event.get_time() + self._computer2.t_i(), COMPUTER2_EVENT
                    )
                    # кладем заявку из буферной памяти в компьютер 1
                    self._sbs.add_event(next_event)
                    # компьютер 1 обрабатывает заявку
                    self._computer2.set_state("busy")

        return count_tasks_refused, count_tasks_processed, total_count_tasks, count_tasks_refused / total_count_tasks, total_count_tasks


# def main():
#     event_approach = EventApproach(
#         client=Client(UniformDistribution(8, 12)),
#         buffer_memory1=BufferMemory(),
#         buffer_memory2=BufferMemory(),
#         computer1=Computer(15),
#         computer2=Computer(30),
#         operator1=Operator(UniformDistribution(15, 25)),
#         operator2=Operator(UniformDistribution(30, 50)),
#         operator3=Operator(UniformDistribution(20, 60)),
#         count_tasks=300
#     )

#     count_tasks_refused, count_tasks_processed, refuse_prob = event_approach.run()

#     print(f"count_tasks_refused = {count_tasks_refused}")
#     print(f"count_tasks_processed = {count_tasks_processed}")
#     print(f"refuse_prob = {refuse_prob}")


# if __name__ == '__main__':
#     main()
