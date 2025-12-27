import torch.nn as nn
import torchvision.models as models

class GlowvaiModel(nn.Module):
    def __init__(self):
        super().__init__()
        base = models.efficientnet_b0(weights="IMAGENET1K_V1")
        self.features = base.features
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.head = nn.Linear(1280, 13)  # MUST match training

    def forward(self, x):
        x = self.features(x)
        x = self.pool(x).flatten(1)
        return self.head(x)
