from pydantic import BaseSettings


class Settings(BaseSettings):
    ADMIN_SDK_SETTINGS: str
    FIREBASE_SETTINGS: str
    MINIO_SERVER: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET_NAME: str

    class Config:
        env_file = '.env'
