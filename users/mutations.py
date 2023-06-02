import bcrypt
from graphql import GraphQLError
from sqlmodel import Session
import strawberry
from common.types import Success
from core.settings import Setting
from users.models import Token, User

from users.types import Login, LoginInput, ResgisterInput, TokenType, UserType
from users.utils import decode_token, generate_token


@strawberry.type
class UserMutations:
    @strawberry.mutation
    def register(self, input: ResgisterInput, secret_code: str) -> Success[UserType]:
        if secret_code != Setting.SECRET_CODE:
            raise GraphQLError("Invalid code")
        with Session(Setting.DB_ENGINE) as session:
            if input.password_1 == input.password_2:
                user = User.new(session=session, input=input)\
                    .set_passwrod(session=session, password=input.password_1)\
                    .gql()
                return Success(success=True, data=user)
            raise GraphQLError("passwords do not match")

    @strawberry.mutation
    def login(self, input: LoginInput) -> Success[Login]:
        with Session(Setting.DB_ENGINE) as session:
            user = User.get(session=session, email=input.email)
            assert user.passwd_hash, GraphQLError("password login not found. Try Google login")
            if bcrypt.checkpw(input.password.encode(), str(user.passwd_hash).encode()):
                token = generate_token(session=session, user=user)
                assert (token.value().token and token.value().refresh_token), GraphQLError("failed to generate token")
                token_gql = token.gql()
                login_data = Login(token=token_gql.token, refresh_token=token_gql.refresh_token, user=user.gql())
                return Success(success=True, data=login_data)
            raise GraphQLError("Please enter valid details")


    @strawberry.mutation
    def refresh_token(self, refresh_token: str) -> Success[TokenType]:
        with Session(Setting.DB_ENGINE) as session:
            decoded = decode_token(refresh_token)
            token_id = decoded.get("token_id")
            assert token_id, GraphQLError("Authentication failded: missing token_id")
            old_token = Token.objects(session).get(token_id=int(token_id))
            new_token = generate_token(session, user=old_token.value().user)
            old_token.delete()
            return Success(success=True, data=new_token.gql())
