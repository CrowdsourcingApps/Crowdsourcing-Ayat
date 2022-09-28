from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.routes import init_api
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


init_api(app)
