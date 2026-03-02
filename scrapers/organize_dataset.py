import os
import shutil
import json

def organize_dataset():
    # Load original symbol data to get mapping/names
    with open('data/symbols_data.json', 'r') as f:
        symbols = json.load(f)

    # Base images directory
    base_images_dir = 'data/images'
    expansion_images_dir = 'data/images/expansion'
    dataset_dir = 'data/dataset'

    os.makedirs(dataset_dir, exist_ok=True)

    # 1. Organize base images
    print("Organizing base images...")
    base_files = [f for f in os.listdir(base_images_dir) if f.endswith('.jpg')]
    for filename in base_files:
        # Extract class name from filename (e.g., check_engine_light.jpg)
        class_name = filename.rsplit('.', 1)[0]
        class_dir = os.path.join(dataset_dir, class_name)
        os.makedirs(class_dir, exist_ok=True)
        shutil.copy(os.path.join(base_images_dir, filename), os.path.join(class_dir, filename))

    # 2. Organize expansion images
    print("Organizing expansion images...")
    if os.path.exists(expansion_images_dir):
        expansion_files = [f for f in os.listdir(expansion_images_dir) if f.endswith('.jpg')]
        for filename in expansion_files:
            # Expansion filenames look like check_engine_alt.jpg
            # We need to map back to the original class name
            class_name = filename.replace('_alt.jpg', '')
            class_dir = os.path.join(dataset_dir, class_name)
            os.makedirs(class_dir, exist_ok=True)
            shutil.copy(os.path.join(expansion_images_dir, filename), os.path.join(class_dir, filename))

    # Count images per class
    counts = {}
    for class_name in os.listdir(dataset_dir):
        class_path = os.path.join(dataset_dir, class_name)
        if os.path.isdir(class_path):
            counts[class_name] = len(os.listdir(class_path))
    
    print(f"Dataset organized. Total classes: {len(counts)}")
    print(f"Classes with more than 1 image: {len([k for k, v in counts.items() if v > 1])}")

if __name__ == "__main__":
    organize_dataset()
