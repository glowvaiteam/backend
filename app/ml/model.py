import torch
from app.ml.model_arch import GlowvaiModel  # same architecture

MODEL_PATH = "models/glowvai_model.pth"

def load_model():
    model = GlowvaiModel()
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
    model.eval()
    return model
