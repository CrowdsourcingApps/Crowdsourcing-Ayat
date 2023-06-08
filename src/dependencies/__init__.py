import json

import firebase_admin
import pyrebase
from azure.storage.blob import BlobServiceClient
from firebase_admin import credentials

from src.settings import settings
from src.settings.logging import logger

admin_sdk = json.loads(settings.ADMIN_SDK_SETTINGS, strict=False)
cred = credentials.Certificate(admin_sdk)
firbase_admin = firebase_admin.initialize_app(cred)

firebase_setting = json.loads(settings.FIREBASE_SETTINGS, strict=False)

firbase = pyrebase.initialize_app(firebase_setting)

db = firbase.database()

connect_str = settings.AZURE_CONNECT_STR
container_name = settings.AZURE_CONTAINER_NAME
try:
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)
except Exception as ex:
    logger.exception(f'[Azure blob] - Problem in intilizing Azure blob service'
                     f' settings. error: {ex}')
