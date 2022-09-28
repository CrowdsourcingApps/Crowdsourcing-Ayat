import json

import firebase_admin
import pyrebase
from firebase_admin import credentials

from src.settings import settings

cred = credentials.Certificate(settings.FIREBASE_ADMIN_CRED_PATH)
firbase_admin = firebase_admin.initialize_app(cred)
firbase = pyrebase.initialize_app(
    json.load(open(settings.FIREBASE_CONFIG_PATH)))

db = firbase.database()
