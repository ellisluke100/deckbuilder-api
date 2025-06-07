from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr


class Config(BaseSettings):
    mongo_addr: str = Field(default="mongodb://localhost:27017")
    # mongo_user: str
    # mongo_password: SecretStr[str]


config = Config()
