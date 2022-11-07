from tempfile import NamedTemporaryFile
from typing import IO, BinaryIO, Tuple

from pydub import AudioSegment
from pydub.silence import split_on_silence

from src.dependencies import minio_client
from src.settings import settings
from src.settings.logging import logger


def upload_file(new_file_name: str, audio_file_path: str) -> bool:
    """ Upload file to minio server"""
    try:
        minio_client.fput_object(
            settings.MINIO_BUCKET_NAME, new_file_name, audio_file_path
        )
        return True
    except Exception as ex:
        logger.exception('[MinIO] - Upload audio file to MinIo server'
                         f' error: {ex}')
        return False


def process_audio(file: BinaryIO) -> Tuple[int, str]:
    """ Get the lenght of audio and convert it to standarized wav"""
    temp: IO = NamedTemporaryFile(delete=False)
    audio_seg = AudioSegment.from_file(file)
    audio_seg = audio_seg.set_channels(1)  # 1 channel (mono)
    audio_seg = audio_seg.set_frame_rate(16000)  # frequency 16khz
    audio_seg = audio_seg.set_sample_width(2)  # bit depth = 2 Byte = 16 bits
    # A suitable value for silence_thresh might be around -50 to -35
    audio_chunks = split_on_silence(audio_seg,
                                    min_silence_len=100,
                                    silence_thresh=-45,
                                    keep_silence=50
                                    )
    # Putting the file back together
    combined = AudioSegment.empty()
    for chunk in audio_chunks:
        combined += chunk
    combined.export(temp, format='wav')
    duration_ms = len(audio_seg)
    return duration_ms, temp.name
