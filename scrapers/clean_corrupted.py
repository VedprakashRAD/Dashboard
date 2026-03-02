from PIL import Image
import os

def clean_corrupted_images(dataset_dir):
    corrupted = 0
    total = 0
    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                total += 1
                path = os.path.join(root, file)
                try:
                    with Image.open(path) as img:
                        img.verify()
                    # Re-open to be sure (verify() doesn't catch everything)
                    with Image.open(path) as img:
                        img.transpose(Image.FLIP_LEFT_RIGHT)
                except Exception as e:
                    print(f"Deleting corrupted image: {path} - Error: {e}")
                    os.remove(path)
                    corrupted += 1
    
    print(f"Scan complete. Found and removed {corrupted} corrupted images out of {total}.")

if __name__ == "__main__":
    clean_corrupted_images('data/dataset')
