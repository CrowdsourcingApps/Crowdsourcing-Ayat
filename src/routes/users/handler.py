from src.dependencies import db
from src.routes.users.schema import UserMetaData
from src.settings.logging import logger


def add_user(user: dict) -> bool:
    try:
        db.child('users').child(user['client_id']).set(user)
        return True
    except Exception as ex:
        logger.exception('[Firebase] - Add new user to users node error:'
                         f' {ex}')
        return False


def update_user(user: dict) -> bool:
    try:
        db.child('users').child(user['client_id']).update(user)
        return True
    except Exception as ex:
        logger.exception('[Firebase] - Update new user error:'
                         f' {ex}')
        return False


def get_user(client_id: str) -> UserMetaData:
    try:
        user_info = db.child('users').child(client_id).get()
        if user_info.pyres is None:
            return None
        try:
            user_meta_data_obj = UserMetaData.parse_obj(user_info.val())
            return user_meta_data_obj
        except Exception as ex:
            logger.exception('Parsing firebase user object to UserMetaData'
                             f' object error: {ex}')
            return None
    except Exception as ex:
        logger.exception(f'[Firebase] - get user from users node error: {ex}')
        return None
