from tempfile import NamedTemporaryFile
from typing import IO, BinaryIO, Tuple

import noisereduce as nr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from scipy.io import wavfile

from src.dependencies import blob_service_client, container_name
from src.settings.logging import logger


def upload_file(new_file_name: str, audio_file_path: str) -> bool:
    """ Upload file to minio server"""
    try:
        blob_client = blob_service_client.get_blob_client(
            container=container_name,
            blob=new_file_name)
        with open(audio_file_path, 'rb') as data:
            blob_client.upload_blob(data)
        return True
    except Exception as ex:
        logger.exception('[Azure blob] - Upload audio file to Azure blob'
                         f' error: {ex}')
        return False


def process_audio(file: BinaryIO) -> Tuple[int, str]:
    """ Get the lenght of audio and convert it to standarized wav"""

    """ step 1: Standarize the audio file by converting it to a mono wav
                with 16khz frequency and 16 bit depth """
    temp: IO = NamedTemporaryFile(delete=False)
    audio_seg = AudioSegment.from_file(file)
    audio_seg = audio_seg.set_channels(1)  # 1 channel (mono)
    audio_seg = audio_seg.set_frame_rate(16000)  # frequency 16khz
    audio_seg = audio_seg.set_sample_width(2)  # bit depth = 2 Byte = 16 bits
    audio_seg.export(temp, format='wav')

    """ step 2: remove silence segments from the audio file """
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

    """ step 3: remove the background noise from the audio file """
    rate, data = wavfile.read(temp)
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wavfile.write(temp, rate, reduced_noise)

    duration_ms = len(audio_seg)
    return duration_ms, temp.name
