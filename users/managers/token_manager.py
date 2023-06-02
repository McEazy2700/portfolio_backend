from graphql import GraphQLError
from sqlmodel import Session, select
from typing import Self

from common.interfaces import ModelManager
from common.utils.graphql import model_to_graphql
from users.models import Token, User
from users.types import TokenType


class TokenManager(ModelManager):
    def __init__(self, session: Session) -> None:
        self.model = Token
        self.__value: Token
        self.fields = ["token", "refresh_token", "user"]
        super().__init__(session)
    
    def get(self, token_id: int) -> Self:
        stmt = select(self.model).where(self.model.id==token_id)
        token = self.session.exec(stmt).one()
        self.__value = token
        return self

    def new(self, user: User) -> Self:
        assert user.id, GraphQLError("User id is required to create token")
        token = self.model(user_id=user.id)
        self.session.add(token)
        self.session.commit()
        self.session.refresh(token)
        self.__value = token
        return self

    def delete(self):
        self.session.delete(self.__value)
        self.session.commit()

    def set_tokens(self, token: str, refresh_token: str) -> Self:
        self.__value.token = token
        self.__value.refresh_token = refresh_token
        self.session.add(self.__value)
        self.session.commit()
        self.session.refresh(self.__value)
        return self

    def value(self) -> Token:
        return self.__value

    def gql(self) -> TokenType:
        self.__value.user
        self.__value.user.profile
        if self.__value.user.profile:
            self.__value.user.profile.image
        return model_to_graphql(TokenType, self.__value, self.fields)
