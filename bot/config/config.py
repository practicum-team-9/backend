from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Подтягивам из .env необходимые параметры."""

    # Токен бота.
    BOT_TOKEN: str

    # Данные для подключения к БД.
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    POSTGRES_DB: str

    # Данные для работы со SpeechKit.
    SPEECH_KIT_API_KEY: str
    SPEECH_KIT_URL: str
    VOICE_LANG: str
    VOICE_NAME: str

    # Данные для работы с Яндекс Формами.
    YANDEX_FORMS_URL: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )


settings = Settings()
