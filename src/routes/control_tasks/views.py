from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies.auth import firebase_authentication
from src.routes.auth.handler import get_participant
from src.routes.auth.schema import UserRoleEnum
from src.routes.control_tasks.validate_correctness.handler import (
    Add_validate_correctness_control_tasks_list,
    get_validate_correctness_entrance_exam_list)
from src.routes.control_tasks.validate_correctness.schema import \
    ValidateCorrectnessControlTask

router = APIRouter()


@router.post('/validate_correctness',
             status_code=200,
             responses={401: {'description': 'UNAUTHORIZED'},
                        400: {'description': 'BAD REQUEST'},
                        403: {'description': 'Forbidden'}})
async def add_validate_correctness_control_tasks(
        control_tasks: List[ValidateCorrectnessControlTask],
        user_id=Depends(firebase_authentication)) -> list:
    """ Add list of control tasks related to validate correctness task type"""
    #  check that user is admin
    user = get_participant(user_id)
    if user.user_role != UserRoleEnum.Admin:
        raise HTTPException(status_code=403, detail='you are not authorized')
    result = Add_validate_correctness_control_tasks_list(control_tasks)
    if result is True:
        return {'message': 'Data was uploaded successfully to firbase.'
                ' Please upload audio files to MinIO control-task-bucket'}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Data was not saved successfully',
        )


@router.get('/validate_correctness',
            response_model=List[ValidateCorrectnessControlTask],
            status_code=200,
            responses={401: {'description': 'UNAUTHORIZED'},
                       404: {'description': 'NOT FOUND'},
                       400: {'description': 'BAD REQUEST'}
                       })
async def get_validate_correctness_entrance_exam(
        user_id=Depends(firebase_authentication)) -> list:
    """ get 7 real like tasks to test if the annotator is qualified to
        participate"""
    # validation
    # the user hasn't pass the test related to validate correctness task
    user = get_participant(user_id)
    pass_exam = user.validate_correctness_pass()
    if pass_exam:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Participant already pass the entrance exam',
        )
    # the user can take the test if number of attempts less than five
    # => 7 questions * 5 attempts = 35 question
    if len(user.validate_correctness_answered_questions_test) == 35:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Participant not allowed to attempt more than 5 times',
        )
    # take previous solved questions in case user tried before and didn't pass
    ps_questions = user.validate_correctness_answered_questions_test
    control_tasks = get_validate_correctness_entrance_exam_list(ps_questions)
    if control_tasks is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No tasks available for entrance test',
        )
    # case of remain questions less than 7
    if len(control_tasks) < 7:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No tasks available for entrance test. please try later',
        )
    return control_tasks
