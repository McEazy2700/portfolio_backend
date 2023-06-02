from datetime import timedelta
from sqlmodel import create_engine
from decouple import config
import cloudinary


cloudinary.config(
  cloud_name = str(config("CLOUDINARY_CLOUD_NAME")),
  api_key = str(config("CLOUDINARY_API_KEY")),
  api_secret = str(config("CLOUDINARY_API_SECRET")),
  secure = True
)

class Setting:
    DB_URL = str(config("DB_URL"))
    DB_ENGINE = create_engine(DB_URL)
    SECRET_KEY = str(config("SECRET_KEY"))
    TOKEN_ISSUER = str(config("TOKEN_ISSUER"))
    TOKEN_VALIDITY_DURATION = timedelta(minutes=5)
    REFRESH_TOKEN_VALIDIT_DURATION = timedelta(minutes=10)
    HASHING_ALGORITHIM = "HS256"
    CORS_ALLOWED_ORIGINS = list(str(config("CORS_ALLOWED_ORIGINS")).split(","))
    SECRET_CODE = str(config("SECRET_CODE"))

