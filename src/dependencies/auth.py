from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth

security = HTTPBearer()


def firebase_authentication(
        cred: HTTPAuthorizationCredentials =
        Depends(HTTPBearer(auto_error=False))
):
    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Bearer authentication required',
            headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
        )
    try:
        decoded_token = auth.verify_id_token(cred.credentials)
        uid = decoded_token['uid']
        email = decoded_token['email']
        return {'user_id': uid, 'user_email': email}
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=F'Invalid authentication credentials {err}',
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'})
