from queue_system_components.distributions import UniformDistribution, ErlangDistribution, PoissonDistribution, ExponentialDistribution, NormalDistribution


class Operator:
    """
    Класс реализющий оператора
    """

    def __init__(
        self,
        disctribution: UniformDistribution | ErlangDistribution | PoissonDistribution | ExponentialDistribution | NormalDistribution
    ) -> None:
        """
        Инициализация атрибутов класса
        Если оператор обслуживает заявку в среднем за 10 +- 5 минут, то это равномерное распределение R[5,15]
        """
        self._distribution = disctribution

        self._is_free = True

    def get_operator_task_time(self):
        """
        Метод позволяет получить время следующего освобождения оператора
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
