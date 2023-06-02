from typing import Optional
import strawberry

@strawberry.input
class ResgisterInput:
    email: str
    password_1: str
    password_2: str


@strawberry.input
class LoginInput:
    email: str
    password: str


@strawberry.type
class Login:
    token: str
    refresh_token: str
    user: "UserType"


@strawberry.type
class ProfileType:
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    image: Optional["ImageType"] = None
    user: "UserType"


@strawberry.type
class UserType:
    id: int
    email: str
    profile: ProfileType


@strawberry.type
class TokenType:
    token: str
    refresh_token: str
    user: UserType


from assets.types import ImageType
