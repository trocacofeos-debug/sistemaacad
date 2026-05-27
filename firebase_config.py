import os
import json
import firebase_admin

from firebase_admin import credentials, firestore

# =========================
# RENDER
# =========================

firebase_key = os.getenv("FIREBASE_CREDENTIALS")

if firebase_key:

    cred_dict = json.loads(firebase_key)

    cred = credentials.Certificate(cred_dict)

# =========================
# LOCALHOST
# =========================

else:

    cred = credentials.Certificate("serviceAccountKey.json")

# =========================
# INIT FIREBASE
# =========================

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()