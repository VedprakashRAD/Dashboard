import os
import cv2
import numpy as np
import random
from tqdm import tqdm
from PIL import Image

def expand_classifier_data(src_dir, dst_dir, target_count=100):
    """
    Takes the small set of real images and generates many augmented versions
    for classifier training.
    """
    os.makedirs(dst_dir, exist_ok=True)
    classes = [d for d in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, d))]
    
    for cls in tqdm(classes):
        cls_src = os.path.join(src_dir, cls)
        cls_dst = os.path.join(dst_dir, cls)
        os.makedirs(cls_dst, exist_ok=True)
        
        src_files = [f for f in os.listdir(cls_src) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))]
        if not src_files: continue
        
        for i in range(target_count):
            src_file = random.choice(src_files)
            path = os.path.join(cls_src, src_file)
            try:
                pil_img = Image.open(path).convert('RGB')
                img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            except Exception as e:
                print(f"Skipping {path}: {e}")
                continue
            
            if img is None: continue
            
            # Augmentations
            # 1. Random rotation
            angle = random.uniform(-15, 15)
            h, w = img.shape[:2]
            M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)
            img = cv2.warpAffine(img, M, (w, h), borderValue=(0,0,0))
            
            # 2. Random brightness/contrast
            alpha = random.uniform(0.7, 1.3)
            beta = random.randint(-40, 40)
            img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
            
            # 3. Random Noise
            if random.random() > 0.5:
                noise = np.random.normal(0, 10, img.shape).astype(np.uint8)
                img = cv2.add(img, noise)
                
            # 4. Random minor blur
            if random.random() > 0.7:
                k = random.choice([3, 5])
                img = cv2.GaussianBlur(img, (k, k), 0)
                
            # 5. Random Background (sometimes)
            # Paste the symbol onto a random solid color or noise
            if random.random() > 0.8:
                bg_color = (random.randint(0, 50), random.randint(0, 50), random.randint(0, 50))
                bg = np.full(img.shape, bg_color, dtype=np.uint8)
                # Simple mask for black background symbols
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
                mask_inv = cv2.bitwise_not(mask)
                bg_final = cv2.bitwise_and(bg, bg, mask=mask_inv)
                fg_final = cv2.bitwise_and(img, img, mask=mask)
                img = cv2.add(bg_final, fg_final)

            cv2.imwrite(os.path.join(cls_dst, f"aug_{i}.jpg"), img)

if __name__ == "__main__":
    # We will expand data/dataset into a training-only folder
    expand_classifier_data('data/dataset', 'data/classifier_train_data', target_count=200)
