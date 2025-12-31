from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.auth.auth_routes import router as auth_router
from app.ml.routes import router as ml_router
from app.users.user_routes import router as user_router
from app.admin.admin_routes import router as admin_router
from app.users.activity_routes import router as activity_router



load_dotenv()

app = FastAPI(title="Glowvai Backend")

# ✅ FIXED CORS CONFIG
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8080",
        "https://glowvai.vercel.app",
        "https://glowvai.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(ml_router, prefix="/api/ml", tags=["ML"])
app.include_router(user_router, prefix="/api/user", tags=["User"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])
app.include_router(activity_router, prefix="/api/user", tags=["Activity"])


@app.get("/")
def root():
    return {"message": "Glowvai backend is running"}
