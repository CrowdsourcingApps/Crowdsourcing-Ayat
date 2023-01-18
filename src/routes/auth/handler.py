from src.dependencies import db
from src.routes.auth.schema import UserOutSchema
from src.settings.logging import logger

""" This handler is resposible for adding participant data"""


def add_participant(participant: dict) -> bool:
    try:
        db.child('participants').child(participant['user_id']).set(participant)
        return True
    except Exception as ex:
        logger.exception('[Firebase] - Add new participant to participants'
                         f' node error: {ex}')
        return False


def update_participant(participant: dict) -> bool:
    try:
        node = db.child('participants').child(participant['user_id'])
        node.update(participant)
        return True
    except Exception as ex:
        logger.exception('[Firebase] - Update new participant error:'
                         f' {ex}')
        return False


def get_participant(user_id: str) -> UserOutSchema:
    try:
        participant_info = db.child('participants').child(user_id).get()
        if participant_info.pyres is None:
            return None
        try:
            participant = participant_info.val()
            user_meta_data_obj = UserOutSchema.parse_obj(participant)
            return user_meta_data_obj
        except Exception as ex:
            logger.exception('Parsing firebase participant object to'
                             f' UserOutSchema object error: {ex}')
            return None
    except Exception as ex:
        logger.exception('[Firebase] - get participant from participants'
                         f'node error: {ex}')
        return None
