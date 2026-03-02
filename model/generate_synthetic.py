import os
import cv2
import random
import numpy as np

def generate_synthetic_data(dataset_dir, output_dir, bg_dir, num_samples=2000):
    """
    Creates composite images with multiple dashboard symbols on background images.
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels'), exist_ok=True)
    
    classes = sorted([d for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d))])
    class_to_idx = {cls: i for i, cls in enumerate(classes)}
    
    bg_images = [os.path.join(bg_dir, f) for f in os.listdir(bg_dir) if f.endswith('.jpg')]
    if not bg_images:
        print("No background images found.")
        return

    for i in range(num_samples):
        # Pick a random background
        bg_path = random.choice(bg_images)
        bg = cv2.imread(bg_path)
        if bg is None: continue
        bg = cv2.resize(bg, (640, 640))
        
        h, w, _ = bg.shape
        labels = []
        
        # Add 1-4 random symbols
        num_symbols = random.randint(1, 4)
        for _ in range(num_symbols):
            cls = random.choice(classes)
            cls_idx = class_to_idx[cls]
            cls_path = os.path.join(dataset_dir, cls)
            symbol_files = [f for f in os.listdir(cls_path) if f.endswith('.jpg')]
            if not symbol_files: continue
            
            symbol_path = os.path.join(cls_path, random.choice(symbol_files))
            symbol = cv2.imread(symbol_path)
            if symbol is None: continue
            
            # Simple augmentation: Random brightness
            alpha = random.uniform(0.7, 1.3)
            beta = random.randint(-30, 30)
            symbol = cv2.convertScaleAbs(symbol, alpha=alpha, beta=beta)
            
            # Simple augmentation: Random tiny blur
            if random.random() > 0.7:
                symbol = cv2.GaussianBlur(symbol, (3, 3), 0)

            # Resize symbol to occupy ~15-25% of background
            s_size = random.randint(120, 220)
            symbol = cv2.resize(symbol, (s_size, s_size))
            
            # Random position
            y = random.randint(0, h - s_size)
            x = random.randint(0, w - s_size)
            
            # Simple overlay
            # For dashboard symbols on black backgrounds, we can take the max to preserve the symbol colors better
            roi = bg[y:y+s_size, x:x+s_size]
            bg[y:y+s_size, x:x+s_size] = cv2.max(roi, symbol)
            
            # Calculate YOLO coordinates
            x_center = (x + s_size/2) / w
            y_center = (y + s_size/2) / h
            width = s_size / w
            height = s_size / h
            labels.append(f"{cls_idx} {x_center} {y_center} {width} {height}")
            
        # Save image and label
        img_name = f"synthetic_{i}.jpg"
        cv2.imwrite(os.path.join(output_dir, 'images', img_name), bg)
        with open(os.path.join(output_dir, 'labels', f"synthetic_{i}.txt"), 'w') as f:
            f.write("\n".join(labels))

    print(f"Generated {num_samples} synthetic multi-symbol images.")

if __name__ == "__main__":
    generate_synthetic_data('data/dataset', 'data/yolo_dataset', 'data/background_images')
