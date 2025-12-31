from datetime import datetime
from app.core.firebase import db


# ---------------- TOTAL & ACTIVE USERS ----------------
def get_summary():
    users = list(db.collection("users").stream())
    total_users = len(users)

    today = datetime.utcnow().replace(hour=0, minute=0, second=0)
    active_users = 0

    for u in users:
        data = u.to_dict()
        updated = data.get("updated_at")
        if updated and updated.replace(tzinfo=None) >= today:
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
        created = u.to_dict().get("created_at")
        if not created:
            continue

        dt = created.replace(tzinfo=None)

        if time_range == "Daily":
            key = dt.strftime("%H:00")
        elif time_range == "Weekly":
            key = dt.strftime("%A")
        else:
            key = dt.strftime("%B")

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
    today = datetime.utcnow().replace(hour=0, minute=0, second=0)
    result = []

    users = db.collection("users").stream()
    for u in users:
        data = u.to_dict()
        updated = data.get("updated_at")

        if updated and updated.replace(tzinfo=None) >= today:
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
    today = datetime.utcnow().replace(hour=0, minute=0, second=0)
    count = 0

    analyses = db.collection("analyses").where("uid", "==", uid).stream()
    for a in analyses:
        created = a.to_dict().get("created_at")
        if created and created.replace(tzinfo=None) >= today:
            count += 1

    return count
