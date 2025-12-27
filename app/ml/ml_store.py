from app.core.firebase import db
from datetime import datetime


def save_ml_analysis(uid: str, email: str, image_url: str, report: dict):
    """Save ML analysis result to Firebase for a user.
    
    Args:
        uid: Firebase user ID
        email: User email
        image_url: Cloudflare R2 image URL
        report: ML analysis report dict
    
    Returns:
        Document ID of saved analysis
    """
    # Extract concerns from the real report structure
    skin_concerns = report.get("skin_concerns", {})
    concerns = [
        k for k, v in skin_concerns.items() 
        if v and v.lower() not in ["none", "minimal", "light", "normal"]
    ]
    
    analysis_doc = {
        "uid": uid,
        "email": email,
        "image_url": image_url,
        "report": report,
        "date": datetime.utcnow().isoformat(),
        "skinScore": report.get("portrait_score", 0),
        "concerns": concerns,
    }
    
    doc_ref = db.collection("analyses").add(analysis_doc)
    return doc_ref[1].id


def get_user_ml_history(uid: str):
    """Fetch all ML analysis records for a user from Firebase.
    
    Args:
        uid: Firebase user ID
    
    Returns:
        List of analysis documents sorted by date (newest first)
    """
    try:
        # Query without order_by to avoid composite index requirement
        docs = db.collection("analyses").where("uid", "==", uid).stream()
        history = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            history.append(data)
        
        # Sort by date in Python (newest first)
        history.sort(key=lambda x: x.get("date", ""), reverse=True)
        return history
    except Exception as e:
        print(f"Error fetching ML history: {e}")
        return []


def get_analysis_by_id(uid: str, analysis_id: str):
    """Fetch a specific analysis by ID for a user.
    
    Args:
        uid: Firebase user ID
        analysis_id: Document ID of the analysis
    
    Returns:
        Analysis document with all details, or None if not found
    """
    try:
        doc = db.collection("analyses").document(analysis_id).get()
        if not doc.exists:
            return None
        
        data = doc.to_dict()
        # Verify the analysis belongs to the user
        if data.get("uid") != uid:
            return None
        
        data["id"] = doc.id
        return data
    except Exception as e:
        print(f"Error fetching analysis by ID: {e}")
        return None
