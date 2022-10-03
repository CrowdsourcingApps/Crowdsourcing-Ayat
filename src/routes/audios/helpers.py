from tempfile import NamedTemporaryFile
from typing import IO, BinaryIO, Tuple

from pydub import AudioSegment

from src.dependencies import minio_client
from src.settings import settings


def upload_file(new_file_name: str, audio_file_path: str) -> bool:
    """ Upload file to minio server"""
    try:
        minio_client.fput_object(
            settings.MINIO_BUCKET_NAME, new_file_name, audio_file_path
        )
        return True
    except Exception:
        # TODO log the exception
        return False


def process_audio(file: BinaryIO) -> Tuple[int, str]:
    """ Get the lenght of audio and convert it to wav"""
    temp: IO = NamedTemporaryFile(delete=False)
    audio_seg = AudioSegment.from_file(file)
    audio_seg.export(temp, format='wav')
    duration_ms = len(audio_seg)
    return duration_ms, temp.name
