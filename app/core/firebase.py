import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Read Firebase key from Render environment variable
firebase_key = os.environ.get("firebase_key")

if not firebase_key:
    raise Exception("firebase_key environment variable is missing")

# Convert string JSON → dict
cred_dict = json.loads(firebase_key)

# Initialize Firebase
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

db = firestore.client()
