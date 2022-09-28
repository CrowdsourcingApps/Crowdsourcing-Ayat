from src.dependencies import db


def add_user(user: dict) -> bool:
    try:
        db.child('users').child(user['client_id']).set(user)
        return True
    except Exception:
        # Todo as err log exception
        return False
