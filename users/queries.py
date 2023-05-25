import strawberry
from core.context import Info

from users.types import UserType


@strawberry.type
class UserQueries:
    @strawberry.field
    def me(self, info: Info) -> UserType | None:
        return info.context.user
