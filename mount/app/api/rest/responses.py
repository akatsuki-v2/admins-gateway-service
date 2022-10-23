from typing import Generic
from typing import Literal
from typing import TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class Success(GenericModel, Generic[T]):
    status: Literal["success"]
    data: T


class Error(GenericModel, Generic[T]):
    status: Literal["error"]
    error: T
    message: str
