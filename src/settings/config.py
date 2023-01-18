import json

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

    def get_firebase_settings(self) -> dict:
        """
        Retrieve FIREBASE_SETTINGS and convert it to a Python dictionary
        """
        firebase_settings_str = self.FIREBASE_SETTINGS
        firebase_settings = json.loads(firebase_settings_str)
        return firebase_settings
