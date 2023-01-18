import secrets
import time

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routes import init_api
from src.settings.logging import logger

app = FastAPI()


@app.middleware('http')
async def log_requests(request, call_next):
    # do not register healthcheck
    health_check = request.url.path.__contains__('docs')
    if not health_check:
        """Comment idem because it is not secure according to bandit"""
        """ idem = ''.join(random.choices(
            string.ascii_uppercase + string.digits,k=6))"""
        idem = secrets.token_hex(3)
        logger.info(f'rid={idem} start - "{request.method}" '
                    f'"{request.url.path}"')
        start_time = time.time()

    response = await call_next(request)

    if not health_check:
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        logger.info(f'rid={idem} completed_in={formatted_process_time}ms'
                    f' status_code={response.status_code}')
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


init_api(app)
