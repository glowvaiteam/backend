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


def update_profile(uid: str, data: dict):
    """Update user profile fields. Expects a dict of allowed fields.

    This will set `profile_completed` to True when called.
    """
    ref = db.collection("users").document(uid)
    doc = ref.get()
    if not doc.exists:
        raise Exception("User not found")

    allowed = ["full_name", "age", "gender", "height", "weight", "profile_image", "profile_completed"]
    payload = {k: v for k, v in data.items() if k in allowed}
    payload["profile_completed"] = True
    payload["updated_at"] = datetime.utcnow()

    ref.update(payload)
    return ref.get().to_dict()
