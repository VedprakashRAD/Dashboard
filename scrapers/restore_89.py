import os
import json
import shutil
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def restore_full_89():
    with open('data/symbols_data.json', 'r') as f:
        symbols = json.load(f)
    
    source_images = [f for f in os.listdir('data/images') if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    dataset_dir = 'data/dataset'
    os.makedirs(dataset_dir, exist_ok=True)
    
    restored = 0
    not_found = []
    
    for s in symbols:
        sid = str(s['id'])
        sname = s['name'].lower()
        target_dir = os.path.join(dataset_dir, sid)
        os.makedirs(target_dir, exist_ok=True)
        
        # If already has images, skip
        if any(f.lower().endswith(('.jpg', '.png')) for f in os.listdir(target_dir)):
            continue
            
        # Try to find a match in data/images
        best_match = None
        highest_score = 0
        
        for img_name in source_images:
            score = similar(sname, img_name.replace('_', ' ').replace('.jpg', ''))
            if score > highest_score:
                highest_score = score
                best_match = img_name
        
        if highest_score > 0.6:
            shutil.copy(os.path.join('data/images', best_match), os.path.join(target_dir, f"base_{best_match}"))
            print(f"Restored ID {sid} ({s['name']}) using {best_match} (score: {highest_score:.2f})")
            restored += 1
        else:
            not_found.append((sid, s['name']))

    print(f"\nRestoration Complete. Restored {restored} classes.")
    if not_found:
        print("Still missing images for these IDs:")
        for sid, name in not_found:
            print(f"  {sid}: {name}")

if __name__ == "__main__":
    restore_full_89()
