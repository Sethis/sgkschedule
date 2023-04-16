from pydantic import BaseSettings, SecretStr, PostgresDsn
import os
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    bot_token: SecretStr
    db_url: PostgresDsn

    class Config:
        env_file = os.path.expanduser('~/.env')


config = Settings()
