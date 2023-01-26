from typing import List

from src.routes.auth.handler import get_participant, update_participant


def update_participants_validate_correctness_no(
        user_id: str, solved: int, correct: int,
        questions_ids: List[str]) -> bool:
    participant = get_participant(user_id)
    if participant is None:
        return False
    participant.validate_correctness_solved_control_correct_no = correct
    participant.validate_correctness_solved_control_no = solved
    participant.validate_correctness_answered_questions_test.extend(
        questions_ids)
    participant_dict = dict(participant)
    result = update_participant(participant_dict)
    if result:
        return True
    return False
