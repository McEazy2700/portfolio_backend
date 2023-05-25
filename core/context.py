from functools import cached_property
from strawberry.fastapi import BaseContext
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType

from users.types import UserType
from users.utils import authenticate


class Context(BaseContext):
    @cached_property
    def user(self) -> UserType | None:
        if not self.request:
            return None

        authorization = self.request.headers.get("Authorization", None)
        if not authorization:
            return None
        return authenticate(authorization)


async def get_context() -> Context:
    return Context()

Info = _Info[Context, RootValueType]
