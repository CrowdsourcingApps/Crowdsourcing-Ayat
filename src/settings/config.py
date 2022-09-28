from pydantic import BaseSettings


class Settings(BaseSettings):
    FIREBASE_ADMIN_CRED_PATH: str
    FIREBASE_CONFIG_PATH: str

    class Config:
        env_file = ".env"
