import os
import random
import cv2
import json
from ultralytics import YOLO

def bulk_test(v8_path, num_images=30, output_dir='data/test_results_bulk'):
    os.makedirs(output_dir, exist_ok=True)
    
    # Load model
    model = YOLO(v8_path)
    
    # Load symbol metadata for readable names
    with open('data/symbols_data.json', 'r') as f:
        symbols_data = json.load(f)
        id_to_name = {str(s['id']): s['name'] for s in symbols_data}

    # Collect all available images
    all_images = []
    
    # Check synthetic images
    synth_dir = 'data/yolo_dataset/images'
    if os.path.exists(synth_dir):
        all_images.extend([os.path.join(synth_dir, f) for f in os.listdir(synth_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        
    # Check original images
    base_dir = 'data/images'
    if os.path.exists(base_dir):
        all_images.extend([os.path.join(base_dir, f) for f in os.listdir(base_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

    if not all_images:
        print("No images found for testing.")
        return

    # Select 30 random images
    test_samples = random.sample(all_images, min(num_images, len(all_images)))
    
    print(f"Starting bulk test on {len(test_samples)} images...\n")
    print(f"{'#':<3} | {'Image Name':<30} | {'Detections (Confidence)'}")
    print("-" * 70)

    for i, img_path in enumerate(test_samples, 1):
        img_name = os.path.basename(img_path)
        # Lower threshold to 0.05 to ensure we see the model's best guesses
        results = model(img_path, conf=0.05, verbose=False)
        
        detections = []
        for box in results[0].boxes:
            cls_id = results[0].names[int(box.cls[0])]
            name = id_to_name.get(cls_id, f"ID:{cls_id}")
            conf = float(box.conf[0])
            detections.append(f"{name} ({conf:.2f})")
        
        det_str = ", ".join(detections) if detections else "No symbols detected"
        print(f"{i:<3} | {img_name[:30]:<30} | {det_str}")
        
        # Save visual result
        results[0].save(filename=os.path.join(output_dir, f'test_{i}_{img_name}'))

    print(f"\nBulk test complete! Visual results saved to: {output_dir}")

if __name__ == "__main__":
    bulk_test('model/weights/best_symbol_model.pt')
