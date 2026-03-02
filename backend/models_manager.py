import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from ultralytics import YOLO
import json
import os

class ModelManager:
    def __init__(self, 
                 detector_path='model/weights/best_detector.pt',
                 classifier_path='model/weights/best_classifier.pth',
                 mapping_path='model/weights/classifier_mapping.json'):
        
        self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        
        # 1. Load Detector (YOLO)
        self.detector = None
        if os.path.exists(detector_path):
            self.detector = YOLO(detector_path)
            
        # 2. Load Classifier (ResNet50 — matches trained weights)
        self.classifier = None
        self.id_to_class = {}
        
        if os.path.exists(classifier_path) and os.path.exists(mapping_path):
            with open(mapping_path, 'r') as f:
                self.id_to_class = json.load(f)
            
            num_classes = len(self.id_to_class)
            self.classifier = models.resnet50()
            num_ftrs = self.classifier.fc.in_features
            self.classifier.fc = nn.Linear(num_ftrs, num_classes)
            
            self.classifier.load_state_dict(torch.load(classifier_path, map_location=self.device))
            self.classifier.to(self.device)
            self.classifier.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def predict(self, image_path, confidence=0.25):
        if not self.detector or not self.classifier:
            return []

        # Step 1: Detect with YOLO
        results = self.detector(image_path, conf=confidence, verbose=False)
        img_orig = Image.open(image_path).convert('RGB')
        
        detections = []
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                # Step 2: Crop detected region
                crop = img_orig.crop((x1, y1, x2, y2))
                
                # Step 3: Classify with ResNet50
                input_tensor = self.transform(crop).unsqueeze(0).to(self.device)
                with torch.no_grad():
                    output = self.classifier(input_tensor)
                    probabilities = torch.nn.functional.softmax(output, dim=1)
                    top_conf, predicted = torch.max(probabilities, 1)
                    class_idx = str(predicted.item())
                    symbol_id = self.id_to_class.get(class_idx)
                    cls_confidence = float(top_conf.item())
                
                detections.append({
                    "symbol_id": symbol_id,
                    "box": [x1, y1, x2, y2],
                    "detector_conf": float(box.conf[0]),
                    "classifier_conf": cls_confidence
                })
        
        # Sort by combined confidence and deduplicate by symbol_id
        detections.sort(key=lambda d: d['detector_conf'] * d['classifier_conf'], reverse=True)
        seen = set()
        unique = []
        for d in detections:
            if d['symbol_id'] not in seen:
                seen.add(d['symbol_id'])
                unique.append(d)
        
        return unique

# Global instance
model_manager = None
def get_model_manager():
    global model_manager
    if model_manager is None:
        model_manager = ModelManager()
    return model_manager
