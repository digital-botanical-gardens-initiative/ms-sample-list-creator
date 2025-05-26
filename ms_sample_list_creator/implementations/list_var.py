from typing import Callable, List


class ListVar:
    def __init__(self, initial: List[str] = []):
        self._value = initial
        self._callbacks: List[Callable[[], None]] = []

    def get(self) -> List[str]:
        return self._value

    def set(self, item: str) -> None:
        self._value.append(item)
        self._notify()

    def _notify(self) -> None:
        for cb in self._callbacks:
            cb()
