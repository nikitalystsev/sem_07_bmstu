from queue_system_components.distributions import UniformDistribution, ErlangDistribution, PoissonDistribution, ExponentialDistribution, NormalDistribution


class Client:
    """
    Класс реализющий клиента (он же генератор)
    """

    def __init__(
        self,
        disctribution: UniformDistribution | ErlangDistribution | PoissonDistribution | ExponentialDistribution | NormalDistribution
    ) -> None:
        """
        Инициализация атрибутов класса
        Если клиент приходят в ИЦ через интервал времени 10 +- 5 минут, то это равномерное распределение R[5,15]
        """

        self._distribution = disctribution

    def gen_next_task_time(self):
        """
        Метод возвращает псевдослучайное число -- время после времени предыдущей заявки, через которое появится новая заявка
        """

        return self._distribution.t_i()
