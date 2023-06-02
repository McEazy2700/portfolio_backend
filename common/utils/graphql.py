from typing import List, Type, TypeVar
from sqlmodel import SQLModel


T = TypeVar("T")
M = TypeVar("M", bound=SQLModel)

def model_to_graphql(gql: Type[T], instance: M, fields: List[str]) -> T:
    kwargs = {}
    for item in instance.__sqlmodel_relationships__:
        getattr(instance, item)
    for item in instance.__dict__.keys():
        if item in fields:
            kwargs[item] = instance.__dict__.get(item, None)
    return gql(**kwargs)
