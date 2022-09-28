from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.dependencies import firbase
from src.dependencies.auth import firebase_authentication
from src.routes.auth.schema import Token, UserOutSchema

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
    except Exception:
        # To do logging the exception
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    jwt = user['idToken']
    return {'access_token': jwt}


@router.get(
    '/me',
    response_model=UserOutSchema,
    status_code=200,
    responses={401: {'description': 'UNAUTHORIZED'}}
)
async def get_user_info(user=Depends(firebase_authentication)):
    return user
