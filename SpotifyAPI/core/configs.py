from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from typing import ClassVar, Optional
from sqlalchemy.orm.decl_api import DeclarativeMeta
import secrets

class Settings(BaseSettings):

    API_V1_STR: str = "/api"
    DB_URL: ClassVar[str] = "mysql+aiomysql://thiagomares:Ferreira13@localhost:3306/musicas"
    DBBaseModel: ClassVar[DeclarativeMeta] = declarative_base()

    JWT_SECRET: str = ''
    ALGORITHM: str = 'HS256'
    class Config:
        case_sensitive = True

settings = Settings()
token = secrets.token_urlsafe(32)