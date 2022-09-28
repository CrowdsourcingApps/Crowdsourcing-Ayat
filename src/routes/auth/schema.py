from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    # refresh_token: str
    # token_type: str


class UserOutSchema(BaseModel):
    user_id: str
    user_email: str
