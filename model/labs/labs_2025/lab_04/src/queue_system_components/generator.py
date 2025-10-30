
from distributions import UniformDistribution, ErlangDistribution, PoissonDistribution, ExponentialDistribution, NormalDistribution


class Generator:
    """
    Класс генератора заявок СМО
    """

    def __init__(
        self,
        disctribution: UniformDistribution | ErlangDistribution | PoissonDistribution | ExponentialDistribution | NormalDistribution
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self._distribution = disctribution

    def gen_next_task_time(self):
        """
        Метод возвращает псевдослучайное число -- время после времени предыдущей заявки, через которое появится новая заявка
        """

        return self._distribution.t_i()
