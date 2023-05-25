from typing import Optional, Union
import strawberry

from common.types import Error, Success

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


from assets.types import ImageType
