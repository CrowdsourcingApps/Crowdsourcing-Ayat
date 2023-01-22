from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies.auth import firebase_authentication
from src.routes.auth.handler import get_participant
from src.routes.auth.schema import UserRoleEnum
from src.routes.control_tasks.validate_correctness.handler import \
    Add_validate_correctness_control_tasks_list
from src.routes.control_tasks.validate_correctness.schema import \
    ValidateCorrectnessControlTask

router = APIRouter()


@router.put('',
            status_code=200,
            responses={401: {'description': 'UNAUTHORIZED'},
                       400: {'description': 'BAD REQUEST'},
                       403: {'description': 'Forbidden'}})
async def validate_correctness_control_tasks(
        control_tasks: List[ValidateCorrectnessControlTask],
        user_id=Depends(firebase_authentication)) -> list:
    """ Add list of control tasks related to validate correctness task type"""
    #  check that user is admin
    user = get_participant(user_id)
    if user.user_role != UserRoleEnum.Admin:
        raise HTTPException(status_code=403, detail='you are not authorized')
    result = Add_validate_correctness_control_tasks_list(control_tasks)
    if result is True:
        return {}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='participant data was not saved successfully',
        )
