from src.dependencies import db
from src.routes.users.schema import UserMetaData


def add_user(user: dict) -> bool:
    try:
        db.child('users').child(user['client_id']).set(user)
        return True
    except Exception:
        # TODO as err log exception
        return False


def get_user(client_id: str) -> UserMetaData:
    try:
        user_info = db.child('users').child(client_id).get()
        if user_info.pyres is None:
            return None
        return UserMetaData.parse_obj(user_info.val())
    except Exception:
        # TODO as err log exception
        return None
