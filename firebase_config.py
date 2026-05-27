import os
import json
import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

firebase_key = os.getenv("FIREBASE_CREDENTIALS")

cred_dict = json.loads(firebase_key)

cred = credentials.Certificate(cred_dict)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()