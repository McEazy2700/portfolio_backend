from typing import Any
import jwt
from datetime import datetime, timezone
from sqlmodel import Session
from core.settings import Setting
from users.managers.token_manager import TokenManager
from users.models import Token, User
from users.types import UserType


class AuthenticationError(Exception):
    pass

def generate_token(session: Session, user: User) -> TokenManager:
    token = Token.objects(session=session).new(user=user)
    payload = {
        "token_id": token.value().id,
        "iss": Setting().TOKEN_ISSUER,
        "iat": datetime.now(tz=timezone.utc)
    }
    token_payload = {
            **payload,
            "exp": datetime.now(tz=timezone.utc) + Setting.TOKEN_VALIDITY_DURATION
        }
    refresh_token_payload = {
            **payload,
            "exp": datetime.now(tz=timezone.utc) + Setting.REFRESH_TOKEN_VALIDIT_DURATION
        }
    token_str = jwt.encode(
            {**token_payload, },
            Setting().SECRET_KEY,
            algorithm=Setting().HASHING_ALGORITHIM
        )
    refresh_token = jwt.encode(
            {**refresh_token_payload},
            Setting().SECRET_KEY,
            algorithm=Setting().HASHING_ALGORITHIM
        )
    token = token.set_tokens(token=token_str, refresh_token=refresh_token)
    return token


def decode_token(token: str) -> dict[str, Any]:
    return dict(jwt.decode(
        token,
        Setting.SECRET_KEY,
        issuer=Setting.TOKEN_ISSUER,
        algorithms=[Setting.HASHING_ALGORITHIM])
    )


def authenticate(authorization: str) -> UserType:
    decoded = decode_token(authorization)
    token_id = decoded.get("token_id")
    assert token_id, AuthenticationError("Authentication failed: token_id not found")
    with Session(Setting.DB_ENGINE) as session:
        token = Token.objects(session=session).get(token_id=int(token_id))
        return token.value().user.gql()
