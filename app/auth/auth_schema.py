from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    uid: str
    full_name: str
    email: EmailStr

class LoginRequest(BaseModel):
    uid: str
