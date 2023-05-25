from typing import Generic, List, Optional, TypeVar

import strawberry


T = TypeVar("T")

@strawberry.input
class PageOptions(Generic[T]):
    offset: Optional[int] = None
    limit: Optional[int] = None
    filter: Optional[T] = None


@strawberry.type
class Success(Generic[T]):
    success: bool
    data: T


@strawberry.type
class Error:
    message: str


class TotalList(Generic[T]):
    def __init__(self, total: int, values: List[T]) -> None:
        self.total: int = total
        self.values: List[T] = values
