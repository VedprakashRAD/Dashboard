import torch
import torchvision.transforms as transforms
from PIL import Image
import os
import io

# Model class (simulated or actual)
class SymbolModel:
    def __init__(self, model_path: str = None):
        # In a real scenario, load the weights from model_path
        # self.model = ...
        pass

    def predict(self, image_bytes: bytes):
        # Preprocessing
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        input_tensor = transform(image).unsqueeze(0)
        
        # Inference (Simulated)
        # with torch.no_grad():
        #     output = self.model(input_tensor)
        
        # Return index of top class (Simulated)
        return 0 # Default to Check Engine Light for now

# Singleton instance
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SymbolModel()
    return _model

def run_inference(image_bytes: bytes):
    model = get_model()
    symbol_index = model.predict(image_bytes)
    return symbol_index
