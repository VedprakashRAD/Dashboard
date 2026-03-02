import os
import cv2
import json

def auto_annotate(data_dir):
    """
    Since our initial dataset consists of isolated symbol images, 
    we can automatically generate bounding boxes that cover most of the image.
    YOLO format: <class_id> <x_center> <y_center> <width> <height> (all normalized 0-1)
    """
    classes = sorted([d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))])
    class_to_idx = {cls: i for i, cls in enumerate(classes)}
    
    # Write classes.txt for YOLO
    with open(os.path.join(data_dir, 'classes.txt'), 'w') as f:
        for cls in classes:
            f.write(f"{cls}\n")

    for cls in classes:
        cls_path = os.path.join(data_dir, cls)
        for img_name in os.listdir(cls_path):
            if not img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            
            img_path = os.path.join(cls_path, img_name)
            img = cv2.imread(img_path)
            if img is None:
                continue
            
            # Since these are symbol-focused images, we assume the symbol occupies 
            # the central 80-90% of the frame.
            # Bounding box: x_center=0.5, y_center=0.5, width=0.8, height=0.8
            label_name = img_name.rsplit('.', 1)[0] + ".txt"
            label_path = os.path.join(cls_path, label_name)
            
            class_id = class_to_idx[cls]
            with open(label_path, 'w') as f:
                # Format: class_id x_center y_center width height
                f.write(f"{class_id} 0.5 0.5 0.8 0.8\n")

    print(f"Auto-annotation complete for {len(classes)} classes.")

if __name__ == "__main__":
    auto_annotate('data/dataset')
