from src.dependencies import db


def add_audio(audio_id, audio: dict) -> bool:
    try:
        db.child('recordings').child(audio_id).set(audio)
        return True
    except Exception:
        # TODO as err log exception
        return False
