from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str


class UserUpdateSchema(BaseModel):
    user_email: str
    validate_correctness_accuracy: int = None
    transcription_accuracy: int = None
    validate_transcription_accuracy: int = None
    number_validate_correctness_tasks: int = 0
    number_transcription_tasks: int = 0
    number_validate_transcription: int = 0


class UserOutSchema(UserUpdateSchema):
    user_id: str


class UserInSchema(BaseModel):
    user_email: str
    password: str


class MessageSchema(BaseModel):
    info: str
