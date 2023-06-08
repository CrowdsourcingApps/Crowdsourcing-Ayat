from pydantic import BaseSettings


class Settings(BaseSettings):
    ADMIN_SDK_SETTINGS: str
    FIREBASE_SETTINGS: str
    AZURE_CONNECT_STR: str
    AZURE_CONTAINER_NAME: str

    class Config:
        env_file = '.env'
