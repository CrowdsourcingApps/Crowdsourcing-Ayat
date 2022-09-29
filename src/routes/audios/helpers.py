from src.dependencies import minio_client
from src.settings import settings


def upload_file(new_file_name: str, audio_file: int) -> bool:
    try:
        minio_client.fput_object(
            settings.MINIO_BUCKET_NAME, new_file_name, audio_file
        )
        return True
    except Exception:
        # TODO log the exception
        return False
