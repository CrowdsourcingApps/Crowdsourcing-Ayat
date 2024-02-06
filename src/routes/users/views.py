import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import Response

from src.dependencies.auth import firebase_authentication
from src.routes.users.handler import add_user, get_user, update_user
from src.routes.users.schema import UserMetaData, UserMetaDataCreate

router = APIRouter()


@router.post('',
             status_code=200,
             response_model=UserMetaData,
             responses={401: {'description': 'UNAUTHORIZED'},
                        400: {'description': 'BAD REQUEST'}})
async def Add_new_reciter(userIn: UserMetaDataCreate,
                          app=Depends(firebase_authentication)):
    app_id = app['user_id']
    user = UserMetaData(**userIn.dict(), create_date=datetime.now(),
                        client_id=str(uuid.uuid4()), application_id=app_id)
    user_dict = dict(user)
    ''' The next line is to avoid  the TypeError:
                "Object of type datetime is not JSON serializable"'''
    user_dict['create_date'] = str(user_dict['create_date'])
    result = add_user(user_dict)
    if result:
        return user
    else:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.put('/{userId}',
            status_code=200,
            response_model=UserMetaData,
            responses={401: {'userIddescription': 'UNAUTHORIZED'},
                       400: {'description': 'BAD REQUEST'},
                       404: {'description': 'NOT FOUND'}})
async def update_reciter_info(userId: str, userIn: UserMetaDataCreate):
    # check if the user with userId is exist
    user = get_user(userId)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'There is no client with id {userId}',
        )

    # update user meta data
    user_dict = dict(userIn)
    user_dict['create_date'] = str(user.create_date)
    user_dict['client_id'] = user.client_id
    result = update_user(user_dict)
    user = UserMetaData(**userIn.dict(), create_date=user.create_date,
                        client_id=user.client_id,
                        application_id=user.application_id)
    if result:
        return user
    else:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
