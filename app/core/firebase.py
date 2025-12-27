import json, os, firebase_admin
from firebase_admin import credentials, firestore

firebase_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")

cred = credentials.Certificate(json.loads(firebase_json))
firebase_admin.initialize_app(cred)

db = firestore.client()
