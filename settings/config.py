from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    CORS_ALLOWED_ORIGINS: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    class Config:
        env_file = "C:/Users/Пользователь/PycharmProjects/test-task-1/.env"

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # @property
    # def database_url_sync(self):
    #     return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


env = Settings()
