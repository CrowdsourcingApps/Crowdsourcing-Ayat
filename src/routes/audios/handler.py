from src.dependencies import db
from src.settings.logging import logger


def add_audio(audio_id, audio: dict) -> bool:
    try:
        db.child('recordings').child(audio_id).set(audio)
        return True
    except Exception as ex:
        logger.exception('[Firebase] - Add new recording to recordings node'
                         f' error: {ex}')
        return False
