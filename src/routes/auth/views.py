import pyrebase
import firebase_admin
import json
from fastapi import APIRouter, Depends, HTTPException, status
from src.routes.auth.schema import Token
from fastapi.security import OAuth2PasswordRequestForm
from firebase_admin import credentials
from src.settings import settings

router = APIRouter()

cred = credentials.Certificate(settings.FIREBASE_ADMIN_CRED_PATH)
firbase_admin = firebase_admin.initialize_app(cred)
firbase = pyrebase.initialize_app(json.load(open(settings.FIREBASE_CONFIG_PATH)))


@router.post(
    '/token',
    response_model=Token,
    status_code=200,
    responses={401: {"description": "UNAUTHORIZED"}},
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
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
