import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import Response

from src.dependencies import firbase
from src.dependencies.auth import firebase_authentication
from src.routes.auth.handler import (add_participant, get_participant,
                                     get_participant_by_email,
                                     update_participant)
from src.routes.auth.schema import (MessageSchema, Token, UserInSchema,
                                    UserOutSchema, UserUpdateSchema)
from src.settings import settings
from src.settings.logging import logger

router = APIRouter()


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
    '/token/refresh',
    response_model=Token,
    status_code=200,
    responses={401: {'description': 'UNAUTHORIZED'},
               400: {'description': 'BAD REQUEST'}},
)
async def refresh_token(refresh_token: str):
    api_key = settings.get_firebase_settings()['apiKey']
    # url = f'https://securetoken.googleapis.com/v1/token?key={api_key}'
    url = 'https://securetoken.googleapis.com/v1/token'
    # The data to be sent in the request body
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    # Make a POST request to the ID token URL
    try:
        response = requests.post(
            url,
            data=data,
            headers={'X-goog-api-key': api_key})
        # Get the new ID token from the response
        response = response.json()
        new_id_token = response['id_token']
        response = Token(access_token=new_id_token,
                         refresh_token=refresh_token)
        return response
    except Exception as ex:
        logger.exception('[Firebase] - Refresh token failed:'
                         f' {ex}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid refresh token'
        )


@router.get(
    '/me',
    response_model=UserOutSchema,
    status_code=200,
    responses={401: {'description': 'UNAUTHORIZED'},
               404: {'description': 'NOT FOUND'}}
)
async def get_participant_info(user_id=Depends(firebase_authentication)):
    # get the additional data for this participants
    participant = get_participant(user_id)
    if participant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'There is no participant with id {user_id}',
        )
    return participant


@router.put(
    '/me/update',
    response_model=UserOutSchema,
    status_code=200,
    responses={401: {'description': 'UNAUTHORIZED'},
               404: {'description': 'NOT FOUND'}}
)
async def update_participant_info(participant_data: UserUpdateSchema,
                                  user_id=Depends(firebase_authentication)):
    # get the additional data for this participants
    participant = get_participant(user_id)
    if participant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'There is no participant with id {user_id}',
        )
    participant_dict = dict(participant_data)
    participant_dict['user_id'] = user_id
    result = update_participant(participant_dict)
    participant = UserOutSchema(**participant_data.dict(), user_id=user_id)
    if result:
        return participant
    else:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.post(
    '/reset_password',
    response_model=MessageSchema,
    status_code=200,
    responses={404: {'description': 'NOT FOUND'},
               400: {'description': 'BAD REQUEST'}}
)
async def send_email_for_reset_password(email: str):
    # check if the email already exist
    if get_participant_by_email(email):
        data = {
            'email': email,
            'requestType': 'PASSWORD_RESET'
        }
        try:
            base_url = 'https://identitytoolkit.googleapis.com/v1/accounts'
            api_key = settings.get_firebase_settings()['apiKey']
            endpoint = 'sendOobCode'
            url = f'{base_url}:{endpoint}'
            response = requests.post(
                url,
                json=data,
                headers={'Content-Type': 'application/json',
                         'X-goog-api-key': api_key}
            )
            response.raise_for_status()
            return MessageSchema(info='Password reset email sent.')
        except Exception as ex:
            logger.exception('[Firebase] - Send email for reset password '
                             f'error: {ex}')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Error while sending email for reset the password'
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'There is no participant with email {email}',
    )
