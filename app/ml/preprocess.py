from PIL import Image
import numpy as np
import io
import requests
import torchvision.transforms as transforms
import mediapipe as mp
from fastapi import HTTPException

# MediaPipe face detector
mp_face = mp.solutions.face_detection
face_detector = mp_face.FaceDetection(
    model_selection=1,
    min_detection_confidence=0.6
)

# Torch transform (must match training)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# --------------------------------------------------
# 1️⃣ EXISTING FUNCTION (BYTES) – KEEP IT
# --------------------------------------------------
def preprocess_image(image_bytes: bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    image_np = np.array(image)
    results = face_detector.process(image_np)

    if not results.detections:
        raise HTTPException(
            status_code=400,
            detail="No face detected. Please upload a clear face image."
        )

    bbox = results.detections[0].location_data.relative_bounding_box
    h, w, _ = image_np.shape

    x1 = int(bbox.xmin * w)
    y1 = int(bbox.ymin * h)
    x2 = int((bbox.xmin + bbox.width) * w)
    y2 = int((bbox.ymin + bbox.height) * h)

    face_crop = image.crop((x1, y1, x2, y2))
    return transform(face_crop)


# --------------------------------------------------
# 2️⃣ NEW FUNCTION (URL) – REQUIRED FOR CLOUDFLARE
# --------------------------------------------------
def preprocess_image_from_url(image_url: str):
    try:
        response = requests.get(image_url, timeout=10)
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to download image")

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Image URL not accessible")

    # Reuse the SAME pipeline
    return preprocess_image(response.content)
