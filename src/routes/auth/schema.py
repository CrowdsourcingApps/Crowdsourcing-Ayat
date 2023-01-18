from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str


class UserOutSchema(BaseModel):
    user_id: str
    user_email: str
    validate_correctness_accuracy: int = None
    transcription_accuracy: int = None
    validate_transcription_accuracy: int = None


class UserInSchema(BaseModel):
    user_email: str
    password: str
