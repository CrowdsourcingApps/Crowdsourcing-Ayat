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


def get_audio_label(audio_file_id: str) -> str:
    try:
        result = db.child('recordings').child(audio_file_id).get()
        if result.pyres is None:
            return 'not_found'
        else:
            recording = result.val()
            label = recording.get('label')
            return label
    except Exception as ex:
        logger.exception('[Firebase] - Get audio label from recordings node'
                         f' error: {ex}')
        return None
