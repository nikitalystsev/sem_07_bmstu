from enum import Enum
from typing import Self


class EventType(Enum):
    GENERATOR = 1
    SERVER = 2


class Event:
    def __init__(self, time: float, event_type: EventType):
        self._time = time
        self._event_type = event_type

    def __lt__(self, other: Self):
        return self._time < other._time

    def __le__(self, other: Self):
        return self._time <= other._time

    def __eq__(self, other: Self):
        return self._time == other._time

    def __ne__(self, other: Self):
        return self._time != other._time

    def __gt__(self, other: Self):
        return self._time > other._time

    def __ge__(self, other: Self):
        return self._time >= other._time

    def __str__(self):
        return f"time: {self._time}, type: {self._event_type}"

    def get_time(self):
        return self._time

    def get_event_type(self):
        return self._event_type
