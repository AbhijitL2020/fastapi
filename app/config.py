from pydantic import BaseSettings


class Settings(BaseSettings):
    database_urlbase: str
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config():
        env_file = ".env"

settings = Settings()                                   # This actually reads the env variables and assigns it to settings
