from typing import Generic, TypeVar, Union

T = TypeVar("T")
E = TypeVar("E")


class Result(Generic[T, E]):
    def __init__(self, value: Union[T, None] = None, error: Union[E, None] = None):
        self.value = value
        self.error = error

    @property
    def is_ok(self) -> bool:
        return self.error is None

    @property
    def is_err(self) -> bool:
        return self.error is not None

    def unwrap(self) -> T:
        if self.is_ok:
            return self.value
        raise Exception(f"Called unwrap on error: {self.error}")

    def unwrap_err(self) -> E:
        if self.is_err:
            return self.error
        raise Exception("Called unwrap_err on a valid result")
