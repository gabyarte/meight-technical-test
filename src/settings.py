import os

from functools import lru_cache
from typing import Optional, Any

from pydantic import field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings

from sqlalchemy import Engine, create_engine

from src.utils import build_db_uri


class Settings(BaseSettings):
    DATABASE_ENGINE: Optional[Engine] = os.getenv('DATABASE_ENGINE', None)

    @field_validator('DATABASE_ENGINE', mode='before')
    def assemble_heroku_db_connection(cls, v: Optional[str],
                                      info: FieldValidationInfo) -> Any:

        url = build_db_uri(
            username=os.environ.get('DATABASE_USER', None),
            password=os.environ.get('DATABASE_PASSWORD', None),
            port=os.environ.get('DATABASE_PORT', None),
            host=os.environ.get('DATABASE_HOST', None),
            database=os.environ.get('DATABASE_DB', None)
        )
        if url is None:
            return None

        return create_engine(url, pool_size=50, echo=False,
                             connect_args={'connect_timeout': 60})


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
