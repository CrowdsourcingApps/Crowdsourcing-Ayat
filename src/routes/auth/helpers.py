# from app.models import User
# from app.utils import auth_handler


# async def authenticate_user(username: str, password: str):
#     user = await User.get_or_none(username=username)
#     if not user:
#         return False
#     if not auth_handler.verify_password(password, user.password_hash):
#         return False
#     return user


# async def exist_user(username: str):
#     user = await User.get_or_none(username=username)
#     if user:
#         return user
#     return False