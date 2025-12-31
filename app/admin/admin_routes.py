from fastapi import APIRouter, Query
from app.admin.admin_service import (
    get_summary,
    get_registrations,
    get_all_users,
    get_today_users,
)

router = APIRouter()


@router.get("/summary")
def summary():
    return get_summary()


@router.get("/registrations")
def registrations(range: str = Query("Daily")):
    return get_registrations(range)


@router.get("/users")
def users():
    return get_all_users()


@router.get("/today-users")
def today_users():
    return get_today_users()
