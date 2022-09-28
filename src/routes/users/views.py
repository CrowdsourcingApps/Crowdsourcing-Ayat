from fastapi import APIRouter, status
from starlette.responses import Response

from src.routes.users.handler import add_user
from src.routes.users.schema import UserMetaData

router = APIRouter()


@router.post('',
             status_code=200,
             responses={401: {'description': 'UNAUTHORIZED'},
                        400: {'description': 'BAD REQUEST'}})
async def Add_new_participant(user: UserMetaData):
    result = add_user(dict(user))
    if result:
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
