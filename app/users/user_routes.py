from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from app.core.security import verify_firebase_user
from app.users.user_store import get_user, update_profile
from app.ml.ml_store import get_user_ml_history
import base64

router = APIRouter()


@router.get("/profile")
def profile(user=Depends(verify_firebase_user)):
    uid = user.get("uid")
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid user")

    # ✅ SAFE: no crash if user doc does not exist
    try:
        user_doc = get_user(uid)
    except:
        user_doc = {
            "uid": uid,
            "full_name": user.get("name"),
            "email": user.get("email"),
            "profile_completed": False,
        }

    history = get_user_ml_history(uid) or []

    return {
        "uid": uid,
        "full_name": user_doc.get("full_name"),
        "email": user_doc.get("email"),
        "age": user_doc.get("age"),
        "gender": user_doc.get("gender"),
        "height": user_doc.get("height"),
        "weight": user_doc.get("weight"),
        "profile_image": user_doc.get("profile_image"),
        "profile_completed": user_doc.get("profile_completed", False),
        "analysis_count": len(history),
        "history": history,
    }



@router.post("/profile")
async def save_profile(
    full_name: str = Form(None),
    age: str = Form(None),
    gender: str = Form(None),
    height: str = Form(None),
    weight: str = Form(None),
    profile_image: UploadFile = File(None),
    user=Depends(verify_firebase_user),
):
    uid = user.get("uid")
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid user")

    # Validate required fields
    if not (age and gender and height and weight):
        raise HTTPException(
            status_code=400,
            detail="Age, Gender, Height, and Weight are required. Profile image is optional."
        )

    image_data = None
    if profile_image is not None:
        contents = await profile_image.read()
        # Store image as base64 data URL
        b64 = base64.b64encode(contents).decode("utf-8")
        mime = profile_image.content_type or "image/png"
        image_data = f"data:{mime};base64,{b64}"

    payload = {
        "full_name": full_name,
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
    }

    if image_data:
        payload["profile_image"] = image_data

    updated = update_profile(uid, payload)

    return updated
