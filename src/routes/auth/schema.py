from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str


class UserUpdateSchema(BaseModel):
    user_email: str

    # number of validate correctness tasks that user solved
    validate_correctness_solved_tasks_no: int = 0

    # number of transcription tasks that users solved
    transcription_solved_tasks_no: int = 0

    # number of validate transcription tasks that users solved
    validate_transcription_solved_tasks_no: int = 0

    # accuracy for each type of task =
    # task type_solved_control_correct_no/task type_solved_control_no
    validate_correctness_solved_control_no: int = 0
    validate_correctness_solved_control_correct_no: int = 0

    transcription_solved_control_no: int = 0
    transcription_solved_control_correct_no: int = 0

    validate_transcription_solved_control_no: int = 0
    validate_transcription_solved_control_correct_no: int = 0


class UserOutSchema(UserUpdateSchema):
    user_id: str


class UserInSchema(BaseModel):
    user_email: str
    password: str


class MessageSchema(BaseModel):
    info: str
