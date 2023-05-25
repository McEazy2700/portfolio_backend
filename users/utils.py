import jwt
from datetime import datetime, timezone
from sqlmodel import Session
from core.settings import Setting
from users.models import Token, User
from users.types import UserType


class AuthenticationError(Exception):
    pass

def generate_token(session: Session, user: User) -> Token:
    token = Token.new(session=session, user=user)
    payload = {
        "token_id": token.id,
        "iss": Setting().TOKEN_ISSUER,
        "iat": datetime.now(tz=timezone.utc)
    }
    token_payload = {
            **payload,
            "exp": datetime.now(tz=timezone.utc) + Setting().TOKEN_VALIDITY_DURATION
        }
    refresh_token_payload = {
            **payload,
            "exp": datetime.now(tz=timezone.utc) + Setting().REFRESH_TOKEN_VALIDIT_DURATION
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
    token = token.set_tokens(session=session, token=token_str, refresh_token=refresh_token)
    return token


def authenticate(authorization: str) -> UserType:
    decoded = dict(jwt.decode(
        authorization,
        Setting().SECRET_KEY,
        issuer=Setting().TOKEN_ISSUER,
        algorithms=[Setting().HASHING_ALGORITHIM])
    )
    token_id = decoded.get("token_id")
    assert token_id, AuthenticationError("Authentication failed; token_id not found")
    with Session(Setting().DB_ENGINE) as session:
        token = Token.get(session=session, token_id=int(token_id))
        return token.user.gql()
