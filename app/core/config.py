from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Базовые настройки приложения."""

    # Дефолтные значения перезаписываются значениями из .env
    app_title: str = 'Название приложения'
    description: str = 'Описание приложения'
    db_type: str = 'Тип базы данных'
    db_api: str = 'API базы данных'
    db_host: str = 'Хост базы данных'
    db_port: str = 'Порт базы данных'
    postgres_user: str = 'Пользователь базы данных'
    postgres_password: str = 'Пароль от базы данных'
    postgres_db: str = 'Название базы данных'

    @property
    def database_url(self):
        """Формируем url для подключения к БД из данных, указанных в .env"""
        return (
            f'{self.db_type}+{self.db_api}://'
            f'{self.postgres_user}:{self.postgres_password}@'
            f'{self.db_host}:{self.db_port}'
            f'/{self.postgres_db}'
        )

    model_config = SettingsConfigDict(env_file='.env', extra='allow')


settings = Settings()
