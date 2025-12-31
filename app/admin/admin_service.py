from datetime import datetime, timedelta, timezone
from app.core.firebase import db

# ================= TIMEZONE =================
IST = timezone(timedelta(hours=5, minutes=30))


def get_today_start():
    now = datetime.now(IST)
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


def to_ist(dt):
    """
    Convert Firestore timestamp (or datetime) to IST safely
    Firestore already returns datetime objects
    """
    if not dt:
        return None

    # Firestore Timestamp -> datetime (already converted by SDK)
    if hasattr(dt, "to_datetime"):
        dt = dt.to_datetime()

    # Ensure timezone awareness
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(IST)


# ---------------- TOTAL & ACTIVE USERS ----------------
def get_summary():
    users = list(db.collection("users").stream())
    total_users = len(users)

    today_start = get_today_start()
    active_users = 0

    for u in users:
        data = u.to_dict()
        last_active = to_ist(data.get("last_active_at"))

        if last_active and last_active >= today_start:
            active_users += 1

    return {
        "total_users": total_users,
        "active_users": active_users,
    }


# ---------------- REGISTRATION GRAPH ----------------
def get_registrations(time_range: str):
    users = db.collection("users").stream()
    buckets = {}

    for u in users:
        created = to_ist(u.to_dict().get("created_at"))
        if not created:
            continue

        if time_range == "Daily":
            key = created.strftime("%d %b")       # 30 Dec
        elif time_range == "Weekly":
            key = created.strftime("%A")          # Monday
        else:
            key = created.strftime("%B")          # December

        buckets[key] = buckets.get(key, 0) + 1

    return {
        "labels": list(buckets.keys()),
        "data": list(buckets.values()),
    }


# ---------------- ALL USERS ----------------
def get_all_users():
    result = []

    users = db.collection("users").stream()
    for u in users:
        data = u.to_dict()

        result.append({
            "id": u.id,
            "full_name": data.get("full_name"),
            "email": data.get("email"),
            "age": data.get("age"),
            "analysis_count": get_total_analysis(u.id),
        })

    return result


# ---------------- TODAY ACTIVE USERS ----------------
def get_today_users():
    today_start = get_today_start()
    result = []

    users = db.collection("users").stream()
    for u in users:
        data = u.to_dict()
        last_active = to_ist(data.get("last_active_at"))

        if last_active and last_active >= today_start:
            result.append({
                "id": u.id,
                "full_name": data.get("full_name"),
                "email": data.get("email"),
                "today_analysis_count": get_today_analysis(u.id),
            })

    return result


# ---------------- HELPERS ----------------
def get_total_analysis(uid: str):
    analyses = db.collection("analyses").where("uid", "==", uid).stream()
    return len(list(analyses))


def get_today_analysis(uid: str):
    today_start = get_today_start()
    count = 0

    analyses = db.collection("analyses").where("uid", "==", uid).stream()
    for a in analyses:
        created = to_ist(a.to_dict().get("created_at"))
        if created and created >= today_start:
            count += 1

    return count
