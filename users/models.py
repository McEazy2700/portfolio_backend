import bcrypt
from typing import TYPE_CHECKING, ClassVar, List, Optional, Self
from graphql import GraphQLError
from pydantic.decorator import validator
from sqlmodel import Field, Relationship, SQLModel, Session, select
from common.utils.graphql import model_to_graphql

from users.types import ResgisterInput, TokenType

if TYPE_CHECKING:
    from assets.models import Image
    from .types import UserType

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    passwd_hash: Optional[str] = Field(default=None)
    tokens: List["Token"] = Relationship(back_populates="user")
    profile: Optional["Profile" ] = Relationship(
            back_populates="user",
            sa_relationship_kwargs=dict(uselist=False))

    @validator("email")
    def validate_email(cls, value:str):
        if "@" not in value or value.split(".").pop() != "com":
            raise GraphQLError("invalid email")

    @classmethod
    def get(cls, session: Session, id: int|None=None, email: str|None=None) -> Self:
        assert id or email, GraphQLError("id or email is required to get user")
        stmt = select(cls)
        if id: stmt = stmt.where(cls.id==id)
        if email: stmt = stmt.where(cls.email==email)
        return session.exec(stmt).one()

    @classmethod
    def new(cls, session: Session, input: ResgisterInput) -> Self:
        user = cls(email=input.email)
        profile = Profile(user=user)
        session.add_all([user, profile])
        session.commit()
        session.refresh(user)
        return user

    def set_passwrod(self, session: Session, password: str) -> Self:
        pass_bytes = password.encode()
        salt = bcrypt.gensalt(rounds=12)
        passwd_hash = bcrypt.hashpw(pass_bytes, salt)
        self.passwd_hash = passwd_hash.decode()
        session.commit()
        session.refresh(self)
        return self

    def gql(self) -> "UserType":
        from .types import UserType
        fields = ["id", "email", "profile"]
        return model_to_graphql(UserType, self, fields=fields)


class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    bio: Optional[str] = Field(default=None)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(
            back_populates="profile",
            sa_relationship_kwargs=dict(foreign_keys="[Profile.user_id]"))

    image_id: Optional[int] = Field(default=None, foreign_key="image.id")
    image: Optional["Image"] = Relationship(
            back_populates="profile",
            sa_relationship_kwargs=dict(foreign_keys="[Profile.image_id]"))


class Token(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    token: Optional[str] = Field(default=None)
    refresh_token: Optional[str] = Field(default=None)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(
            back_populates="tokens",
            sa_relationship_kwargs=dict(foreign_keys="[Token.user_id]"))

    session: ClassVar[Session]

    @classmethod
    def get(cls, session: Session, token_id: int) -> Self:
        cls.session = session
        stmt = select(cls).where(cls.id==token_id)
        token = session.exec(stmt).one()
        return token

    @classmethod
    def new(cls, session: Session, user: User) -> Self:
        cls.session = session
        assert user.id, GraphQLError("User id is required to create token")
        token = cls(user_id=user.id)
        session.add(token)
        session.commit()
        session.refresh(token)
        return token

    def delete(self):
        self.session.delete(self)
        self.session.commit()

    def set_tokens(self, token: str, refresh_token: str) -> Self:
        self.token = token
        self.refresh_token = refresh_token
        self.session.commit()
        self.session.refresh(self)
        return self

    def gql(self) -> TokenType:
        fields = ["token", "refresh_token", "user"]
        return model_to_graphql(TokenType, self, fields)
