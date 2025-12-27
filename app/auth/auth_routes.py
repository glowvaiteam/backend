from fastapi import APIRouter, HTTPException, Depends
from app.auth.auth_schema import SignupRequest, LoginRequest
from app.auth.auth_service import save_user, get_user
from app.core.security import verify_firebase_user

router = APIRouter()

@router.post("/signup")
def signup(data: SignupRequest):
    try:
        return save_user(data.uid, data.full_name, data.email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(data: LoginRequest):
    try:
        return get_user(data.uid)
    except Exception:
        raise HTTPException(status_code=401, detail="Email not registered")

@router.get("/me")
def get_me(user=Depends(verify_firebase_user)):
    return get_user(user["uid"])
