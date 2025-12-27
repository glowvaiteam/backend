from app.core.firebase import db
from datetime import datetime

def save_user(uid: str, full_name: str, email: str):
    ref = db.collection("users").document(uid)

    if ref.get().exists:
        raise Exception("Email already registered")

    ref.set({
        "uid": uid,
        "full_name": full_name,
        "email": email,
        "created_at": datetime.utcnow()
    })

    return {"message": "Signup successful"}

def get_user(uid: str):
    doc = db.collection("users").document(uid).get()
    if not doc.exists:
        raise Exception("User not found")
    return doc.to_dict()
