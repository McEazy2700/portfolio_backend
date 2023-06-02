from abc import ABC, abstractmethod
from typing import Self

from sqlmodel import Session


class ModelManager(ABC):
    def __init__(self, session: Session) -> None:
        self.session = session
        super().__init__()


    @abstractmethod
    def get(self) -> Self:
        pass


    @abstractmethod
    def new(self) -> Self:
        pass
