from fastapi import APIRouter, Depends, FastAPI

from src.dependencies.auth import firebase_authentication
from src.routes.auth import views as auth_views
from src.routes.users import views as users_views

api_router = APIRouter()
api_router.include_router(auth_views.router, tags=['Authentication'])
api_router.include_router(users_views.router,
                          tags=['Users'],
                          prefix='/users',
                          dependencies=[Depends(firebase_authentication)])


def init_api(app: FastAPI) -> None:
    app.include_router(api_router)
