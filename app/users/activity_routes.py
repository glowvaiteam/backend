from fastapi import APIRouter, Depends
from app.core.security import verify_firebase_user
from app.core.firebase import db
from datetime import datetime

router = APIRouter()

@router.post("/active")
def mark_user_active(user=Depends(verify_firebase_user)):
    uid = user.get("uid")

    if not uid:
        return {"status": "error", "message": "Invalid user"}

    db.collection("users").document(uid).update({
        "last_active_at": datetime.utcnow()
    })

    return {"status": "ok"}
