from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    DATABASE_URI: str
    CODE: str
    model_config = SettingsConfigDict(env_file=ROOT_DIR / '.env', extra='ignore')


settings = Settings()
