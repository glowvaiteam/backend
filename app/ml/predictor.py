import torch
import numpy as np
import logging
from app.ml.model_arch import GlowvaiModel

logger = logging.getLogger(__name__)

MODEL_PATH = "models/glowvai_model.pth"
device = torch.device("cpu")

# Load model once
model = None
model_loaded = False

try:
    model = GlowvaiModel().to(device)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.eval()
    model_loaded = True
    logger.info("✅ ML Model loaded successfully")
except Exception as e:
    logger.warning(f"⚠️ Failed to load ML model: {e}. Using random predictions for demo.")
    model_loaded = False


@torch.no_grad()
def predict(image_tensor):
    """Predict skin analysis from image tensor"""
    if not model_loaded or model is None:
        logger.warning("Using mock predictions - model not loaded")
        return mock_predictions(image_tensor)
    
    try:
        image_tensor = image_tensor.to(device)
        preds = model(image_tensor.unsqueeze(0)).squeeze(0).cpu().numpy()
        logger.info(f"Model predictions: {preds}")
        return postprocess_predictions(preds)
    except Exception as e:
        logger.error(f"Prediction error: {e}. Using mock predictions.")
        return mock_predictions(image_tensor)


def mock_predictions(image_tensor):
    """Generate varied mock predictions for testing"""
    # Create predictions with some randomness to simulate different faces
    seed_val = int(image_tensor.sum().item() * 1000) % 100
    np.random.seed(seed_val)
    
    preds = np.random.uniform(0.3, 0.8, 13)
    logger.warning(f"Using mock predictions with seed {seed_val}")
    return postprocess_predictions(preds)


def postprocess_predictions(preds: np.ndarray):
    """
    THIS MUST MATCH report_builder.py KEYS EXACTLY
    """
    return {
        # Required by build_report()
        "portrait_score": int(np.clip(preds[0] * 100, 20, 95)),

        "eyes": int(np.clip(preds[1] * 10, 3, 10)),
        "eyebrows": int(np.clip(preds[2] * 10, 3, 10)),
        "nose": int(np.clip(preds[3] * 10, 3, 10)),
        "lips": int(np.clip(preds[4] * 10, 3, 10)),
        "jawline": int(np.clip(preds[5] * 10, 3, 10)),
        "cheekbones": int(np.clip(preds[6] * 10, 3, 10)),

        "skin_clarity": int(np.clip(preds[7] * 10, 2, 9)),
        "acne_severity": int(np.clip(preds[8] * 5, 0, 5)),
        "dark_spots": int(np.clip(preds[9] * 5, 0, 5)),

        "skin_tone": decode_skin_tone(preds[10] if len(preds) > 10 else np.random.random()),
        "skin_type": decode_skin_type(preds[11] if len(preds) > 11 else np.random.random()),
    }


def decode_skin_tone(value: float):
    if value < 0.33:
        return "Fair"
    elif value < 0.66:
        return "Medium"
    return "Deep"


def decode_skin_type(value: float):
    if value < 0.25:
        return "Dry"
    elif value < 0.5:
        return "Normal"
    elif value < 0.75:
        return "Oily"
    return "Combination"
