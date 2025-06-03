from typing import Generic, Optional, TypeVar, Union

from ms_sample_list_creator.implementations.result_exception import ResultException

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

    def unwrap(self) -> Optional[T]:
        if self.is_ok:
            return self.value
        raise ResultException(f"Called unwrap on error: {self.error}")

    def unwrap_err(self) -> Optional[E]:
        if self.is_err:
            return self.error
        raise ResultException("Called unwrap_err on a valid result")
