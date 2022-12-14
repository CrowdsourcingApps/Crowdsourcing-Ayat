import json

import firebase_admin
import pyrebase
from firebase_admin import credentials
from minio import Minio

from src.settings import settings
from src.settings.logging import logger

admin_sdk = json.loads(settings.ADMIN_SDK_SETTINGS, strict=False)
cred = credentials.Certificate(admin_sdk)
firbase_admin = firebase_admin.initialize_app(cred)

firebase_setting = json.loads(settings.FIREBASE_SETTINGS, strict=False)

firbase = pyrebase.initialize_app(firebase_setting)

db = firbase.database()

minio_client = Minio(
    settings.MINIO_SERVER,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)

bucket_name = settings.MINIO_BUCKET_NAME

# Create the bucket if not exist
try:
    found = minio_client.bucket_exists(bucket_name)
except Exception as ex:
    found = False
    logger.exception(f'[MinIO] - Can not check if bucket {bucket_name} exists.'
                     f' error: {ex}')
if not found:
    try:
        minio_client.make_bucket(bucket_name)
    except Exception as ex:
        logger.exception(f'[MinIO] - Can not create the bucket {bucket_name}.'
                         f'error: {ex}')
