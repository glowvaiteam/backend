from app.core.firebase import db
from datetime import datetime

def save_user(uid: str, full_name: str, email: str):
    ref = db.collection("users").document(uid)

    if ref.get().exists:
        return {"message": "User already exists"}

    ref.set({
        "uid": uid,
        "full_name": full_name,
        "email": email,
        "created_at": datetime.utcnow()
    })

    return {"message": "User saved successfully"}


def get_user(uid: str):
    doc = db.collection("users").document(uid).get()

    if not doc.exists:
        raise Exception("User not found")

    return doc.to_dict()

from datetime import datetime

def update_profile(uid: str, data: dict):
    ref = db.collection("users").document(uid)
    doc = ref.get()

    # ✅ CREATE USER IF NOT EXISTS
    if not doc.exists:
        ref.set({
            "uid": uid,
            "created_at": datetime.utcnow(),
        })

    allowed = [
        "full_name",
        "age",
        "gender",
        "height",
        "weight",
        "profile_image",
        "profile_completed",
    ]

    payload = {k: v for k, v in data.items() if k in allowed}
    payload["profile_completed"] = True
    payload["updated_at"] = datetime.utcnow()

    # ✅ SAFE WRITE (NO CRASH)
    ref.set(payload, merge=True)

    return ref.get().to_dict()
