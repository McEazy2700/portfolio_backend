from typing import Self, Type, TypeVar
from sqlmodel import Session

M = TypeVar("M")
T = TypeVar("T")

class Manager:
    def __init__(self, session: Session, model: Type[M], gql: T) -> None:
        self.session = session
        self.Model = model
        self.GraphqlType = gql



