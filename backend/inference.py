import torch
import json
import os
from ultralytics import YOLO

from .models_manager import get_model_manager

class SymbolInference:
    def __init__(self, data_json_path='data/symbols_data.json'):
        self.manager = get_model_manager()
        
        with open(data_json_path, 'r') as f:
            self.symbols_data = json.load(f)
            self.id_to_data = {str(s['id']): s for s in self.symbols_data}

    def predict(self, image_path, confidence=0.25):
        # Step 1: Execute two-stage pipeline
        detections = self.manager.predict(image_path, confidence=confidence)
        
        if not detections:
            # Check if models are actually loaded
            if not self.manager.detector or not self.manager.classifier:
                return {"status": "error", "message": "Detection models are still initializing or training."}
            
            return {
                "status": "success",
                "message": "No specific dashboard symbols recognized.",
                "symbols": []
            }

        predictions = []
        for det in detections:
            symbol_id = det['symbol_id']
            symbol_data = self.id_to_data.get(str(symbol_id))
            
            if symbol_data:
                predictions.append({
                    "name": symbol_data['name'],
                    "description": symbol_data['description'],
                    "recommendation": symbol_data['recommendation'],
                    "severity": symbol_data['severity'],
                    "startup_behavior": symbol_data.get('startup_behavior', 'N/A'),
                    "persistent_behavior": symbol_data.get('persistent_behavior', 'N/A'),
                    "confidence": det['detector_conf'],
                    "detector_conf": det['detector_conf'],
                    "classifier_conf": det['classifier_conf']
                })

        return {
            "status": "success",
            "symbols": predictions
        }

# Singleton instance
inference_engine = SymbolInference()
