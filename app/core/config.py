import os
import pathlib
import secrets
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
from typing import List, Optional, Union, Any
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    APP_NAME: str
    ENV: str
    ROOT_PATH: str
    API_V1_STR: str
    DOCS_URL: Any = "/docs"
    REDOC_URL: Any = "/redoc"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool
    SQLALCHEMY_DATABASE_URI: str
    NAME_FIRST_SUPERADMIN: str
    EMAIL_FIRST_SUPERADMIN: EmailStr
    PASS_FIRST_SUPERADMIN: str
    DOCUMENT_FIRST_SUPERADMIN: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SECRET_KEY: str = secrets.token_urlsafe(32)
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]

        elif isinstance(v, (list, str)):
            return v

        raise ValueError(v)

    @validator("ROOT_PATH", pre=True)
    def environment_root_path(cls, v: str) -> str:
        load_dotenv()

        if os.getenv("ENV") == "development":
            return ""

        elif os.getenv("ENV") == "production":
            return v

        raise ValueError(v)

    @validator("DOCS_URL", "REDOC_URL", pre=True)
    def environment_docs(cls, v: str) -> Any:
        load_dotenv()

        if os.getenv("ENV") == "development":
            return v

        elif os.getenv("ENV") == "production":
            return None

        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()