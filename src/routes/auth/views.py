from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.dependencies import firbase
from src.dependencies.auth import firebase_authentication
from src.routes.auth.handler import add_participant
from src.routes.auth.schema import Token, UserInSchema, UserOutSchema
from src.settings.logging import logger

router = APIRouter()


@router.post(
    '/token',
    response_model=Token,
    status_code=200,
    responses={401: {'description': 'UNAUTHORIZED'}},
)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = firbase.auth().sign_in_with_email_and_password(
            form_data.username, form_data.password)
    except Exception as ex:
        logger.exception('[Firebase] - Authentication with Firebase failed:'
                         f' {ex}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    jwt = user['idToken']
    refresh_token = user['refreshToken']
    response = Token(access_token=jwt, refresh_token=refresh_token)
    return response


@router.post(
    '/register',
    response_model=Token,
    status_code=200,
    responses={400: {'description': 'BAD REQUEST'}},
)
async def sign_up(
        form_data: UserInSchema):
    try:
        # create new user
        user = firbase.auth().create_user_with_email_and_password(
            form_data.user_email, form_data.password)
        # Add the new user to the participants node with additional data
        user_id = user['localId']
        refresh_token = user['refreshToken']
        participant = UserOutSchema(user_id=user_id,
                                    user_email=form_data.user_email)
        participant_dict = dict(participant)
        if add_participant(participant_dict):
            jwt = user['idToken']
            response = Token(access_token=jwt, refresh_token=refresh_token)
            return response
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='participant data was not saved successfully',
            )
    except Exception as ex:
        logger.exception('[Firebase] - Sign up with Firebase failed:'
                         f' {ex}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email is already exists',
            headers={'WWW-Authenticate': 'Bearer'},
        )


@router.get(
    '/me',
    response_model=UserOutSchema,
    status_code=200,
    responses={401: {'description': 'UNAUTHORIZED'}}
)
async def get_user_info(user=Depends(firebase_authentication)):
    return user
