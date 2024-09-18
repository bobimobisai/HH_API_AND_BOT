from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_CONFIG: dict
    REDIS_CONFIG: dict
    JWT_CONFIG: dict
    GLOBAL_CONFIG: dict

    @property
    def JWT_CONFIG(self):
        return self.JWT_CONFIG    

    @property
    def GLOBAL_CONFIG(self):
        return self.GLOBAL_CONFIG

    @property
    def DATABASE_URL_alembic(self):
        return f"postgresql+psycopg2://{self.DB_CONFIG["user"]}:{self.DB_CONFIG["password"]}@{self.DB_CONFIG["host"]}:{self.DB_CONFIG["port"]}/{self.DB_CONFIG["db_name"]}"

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_CONFIG["user"]}:{self.DB_CONFIG["password"]}@{self.DB_CONFIG["host"]}:{self.DB_CONFIG["port"]}/{self.DB_CONFIG["db_name"]}"

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_CONFIG["user"]}:{self.DB_CONFIG["password"]}@{self.DB_CONFIG["host"]}:{self.DB_CONFIG["port"]}/{self.DB_CONFIG["db_name"]}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
