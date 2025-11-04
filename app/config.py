from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_username: str = "postgres"
    database_password: str = "admin123"
    database_hostname: str
    database_port: str = "5433"
    database_name: str = "fastapi"
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
