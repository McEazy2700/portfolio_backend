import bcrypt
from graphql import GraphQLError
from sqlmodel import Session
import strawberry
from common.types import Success
from core.settings import Setting
from users.models import User

from users.types import Login, LoginInput, ResgisterInput, UserType
from users.utils import generate_token


@strawberry.type
class UserMutations:
    @strawberry.field
    def register(self, input: ResgisterInput) -> Success[UserType]:
        with Session(Setting().DB_ENGINE) as session:
            if input.password_1 == input.password_2:
                user = User.new(session=session, input=input)\
                    .set_passwrod(session=session, password=input.password_1)\
                    .gql()
                return Success(success=True, data=user)
            raise GraphQLError("passwords do not match")

    @strawberry.field
    def login(self, input: LoginInput) -> Success[Login]:
        with Session(Setting().DB_ENGINE) as session:
            user = User.get(session=session, email=input.email)
            assert user.passwd_hash, GraphQLError("password login not found. Try Google login")
            if bcrypt.checkpw(input.password.encode(), str(user.passwd_hash).encode()):
                token = generate_token(session=session, user=user)
                assert token.token and token.refresh_token, GraphQLError("failed to generate token")
                login_data = Login(token=token.token, refresh_token=token.refresh_token, user=user.gql())
                return Success(success=True, data=login_data)
            raise GraphQLError("Please enter valid details")
