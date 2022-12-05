from datetime import datetime

from fastapi import APIRouter, status
from starlette.responses import Response

from src.routes.users.handler import add_user
from src.routes.users.schema import UserMetaData, UserMetaDataCreate

router = APIRouter()


@router.post('',
             status_code=200,
             responses={401: {'description': 'UNAUTHORIZED'},
                        400: {'description': 'BAD REQUEST'}})
async def Add_new_participant(userIn: UserMetaDataCreate):

    user = UserMetaData(**userIn.dict(), create_date=datetime.now())
    user_dict = dict(user)
    ''' The next line is to avoid  the TypeError:
                "Object of type datetime is not JSON serializable"'''
    user_dict['create_date'] = str(user_dict['create_date'])
    result = add_user(user_dict)
    if result:
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
