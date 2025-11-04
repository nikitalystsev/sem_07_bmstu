from queue_system_components.distributions import UniformDistribution, ErlangDistribution, PoissonDistribution, ExponentialDistribution, NormalDistribution


class Server:
    """
    Класс, реализующий обслуживающий аппарат (ОА)
    """

    def __init__(
        self,
        distribution: UniformDistribution | ErlangDistribution | PoissonDistribution | ExponentialDistribution | NormalDistribution
    ):
        """
        Инициализация атрибутов класса
        """
        self._distribution = distribution
        self._is_free = True  # свободен ли

    def get_server_task_time(self):
        """
        Метод позволяет получить время следующего освобождения ОА
        """
        return self._distribution.t_i()

    def set_state(self, state: str):
        """
        Установка состояния ОА
        """
        if state == "free":
            self._is_free = True
        else:
            self._is_free = False

    def is_free(self) -> bool:
        """
        Возвращает состояние ОА
        """
        return self._is_free
