from pydantic import BaseSettings


class Settings(BaseSettings):
    FIREBASE_ADMIN_CRED_PATH: str
    FIREBASE_CONFIG_PATH: str
    MINIO_SERVER: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET_NAME: str

    class Config:
        env_file = '.env'
