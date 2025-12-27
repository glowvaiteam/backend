from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.cloudflare.upload import upload_image_to_cloudflare
from app.ml.preprocess import preprocess_image_from_url
from app.ml.predictor import predict
from app.ml.report_builder import build_report
from app.ml.ml_store import save_ml_analysis, get_user_ml_history, get_analysis_by_id
from app.core.security import verify_firebase_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/analyze-face")
async def analyze_face(image: UploadFile = File(...), user=Depends(verify_firebase_user)):
    """
    Analyze face image (AUTHENTICATED):
    1. Upload to Cloudflare R2
    2. Run ML analysis
    3. Save report to Firebase
    4. Return image URL and report
    """
    uid = user.get("uid")
    email = user.get("email")
    if not uid or not email:
        raise HTTPException(status_code=401, detail="Invalid user")

    # 1️⃣ Read image bytes from frontend
    image_bytes = await image.read()

    # 2️⃣ Upload image to Cloudflare
    image_url = upload_image_to_cloudflare(
        image_bytes=image_bytes,
        content_type=image.content_type
    )

    # 3️⃣ Preprocess image USING URL (not bytes)
    image_tensor = preprocess_image_from_url(image_url)

    if image_tensor is None:
        raise HTTPException(
            status_code=400,
            detail="No face detected. Please upload a clear face image."
        )

    # 4️⃣ ML model prediction
    raw_predictions = predict(image_tensor)

    # 5️⃣ Build human-readable report
    report = build_report(raw_predictions)

    # 6️⃣ Save to Firebase
    analysis_id = save_ml_analysis(uid, email, image_url, report)

    # 7️⃣ Return image link + report + analysis ID
    return {
        "image_url": image_url,
        "report": report,
        "analysis_id": analysis_id
    }


@router.post("/analyze-face-demo")
async def analyze_face_demo(image: UploadFile = File(...)):
    """
    🧪 DEMO/TEST ENDPOINT (NO AUTH REQUIRED)
    Use this to test the ML pipeline without authentication
    """
    logger.info("🧪 Using DEMO endpoint (no auth required)")
    
    # 1️⃣ Read image bytes
    image_bytes = await image.read()

    # 2️⃣ Upload image to Cloudflare
    image_url = upload_image_to_cloudflare(
        image_bytes=image_bytes,
        content_type=image.content_type
    )
    logger.info(f"✅ Image uploaded: {image_url}")

    # 3️⃣ Preprocess image USING URL
    image_tensor = preprocess_image_from_url(image_url)

    if image_tensor is None:
        raise HTTPException(
            status_code=400,
            detail="No face detected. Please upload a clear face image."
        )
    logger.info("✅ Image preprocessed")

    # 4️⃣ ML model prediction
    raw_predictions = predict(image_tensor)
    logger.info(f"✅ Predictions: {raw_predictions}")

    # 5️⃣ Build human-readable report
    report = build_report(raw_predictions)
    logger.info(f"✅ Report built: portrait_score={report.get('portrait_score')}")

    # 7️⃣ Return without saving to Firebase (demo only)
    return {
        "image_url": image_url,
        "report": report,
        "analysis_id": "demo-no-save"
    }


@router.get("/history")
async def get_analysis_history(user=Depends(verify_firebase_user)):
    """Get all ML analysis records for the current user"""
    uid = user.get("uid")
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid user")
    
    history = get_user_ml_history(uid)
    return history


@router.get("/analysis/{analysis_id}")
async def get_analysis_detail(analysis_id: str, user=Depends(verify_firebase_user)):
    """Get detailed analysis report by ID"""
    uid = user.get("uid")
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid user")
    
    analysis = get_analysis_by_id(uid, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return analysis
