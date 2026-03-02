from ultralytics import YOLO
import os

def train_detection():
    # Load a pretrained YOLOv8n model
    model = YOLO('yolov8n.pt') 

    # Train the model
    results = model.train(
        data='data/yolo_dataset/data.yaml',
        epochs=50,
        imgsz=640,
        batch=16,
        name='symbol_detector',
        device='mps', # Use Apple Silicon GPU for faster training
        workers=0,    # Avoid multiprocessing issues on Mac
        project='runs/detect',
        exist_ok=True
    )
    
    print("Optimization: Detection model training complete.")
    # Export the model
    success = model.export(format='onnx')
    print(f"Export success: {success}")

if __name__ == "__main__":
    train_detection()
