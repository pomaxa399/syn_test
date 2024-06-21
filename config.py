from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str = 'BOT_TOKEN'
    admin_id: int = 'ADMIN_ID'

    project_root: Path = Path(__file__).parent.parent.resolve()
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


if __name__ == "__main__":
    print(settings)