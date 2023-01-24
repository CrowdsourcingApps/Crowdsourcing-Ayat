from enum import Enum
from typing import List

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str


class UserRoleEnum(str, Enum):
    Admin = 'admin'
    RecitingApp = 'reciting_app'
    Annotator = 'annotator'


class UserUpdateSchema(BaseModel):
    user_email: str
    user_role: UserRoleEnum = UserRoleEnum.Annotator

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


VALIDATE_CORRECTNESS_THRESHOLD = 0.8


class UserOutSchema(UserUpdateSchema):
    user_id: str
    validate_correctness_answered_questions_test: List[str] = []

    def validate_correctness_accuracy(self):
        if self.validate_correctness_solved_control_no == 0:
            return 0
        solved_all = self.validate_correctness_solved_control_no
        solved_correct = self.validate_correctness_solved_control_correct_no
        accuracy = solved_correct / solved_all
        return accuracy

    def validate_correctness_pass(self):
        accuracy = self.validate_correctness_accuracy()
        return accuracy >= VALIDATE_CORRECTNESS_THRESHOLD


class UserInSchema(BaseModel):
    user_email: str
    password: str


class MessageSchema(BaseModel):
    info: str
