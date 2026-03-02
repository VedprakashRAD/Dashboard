import os
import shutil
import json

def refine_organization():
    # Load original symbol data
    with open('data/symbols_data.json', 'r') as f:
        symbols = json.load(f)

    base_images_dir = 'data/images'
    expansion_images_dir = 'data/images/expansion'
    dataset_dir = 'data/dataset'

    # Clear previous organization
    if os.path.exists(dataset_dir):
        shutil.rmtree(dataset_dir)
    os.makedirs(dataset_dir, exist_ok=True)

    # Helper for very robust normalization
    def normalize(text):
        return text.lower().replace('/', ' ').replace('(', ' ').replace(')', ' ').replace(',', ' ').replace(':', ' ').replace('-', ' ').replace('_', ' ').replace('\u00a0', ' ').strip()

    name_to_id = {}
    for s in symbols:
        norm_name = normalize(s['name'])
        name_to_id[norm_name] = s['id']
        os.makedirs(os.path.join(dataset_dir, str(s['id'])), exist_ok=True)

    # 1. Organize base images
    print("Organizing base images...")
    base_files = [f for f in os.listdir(base_images_dir) if f.endswith('.jpg')]
    for filename in base_files:
        norm_fn = normalize(filename.rsplit('.', 1)[0])
        matched = False
        for norm_name, symbol_id in name_to_id.items():
            if norm_fn == norm_name or norm_fn in norm_name or norm_name in norm_fn:
                shutil.copy(os.path.join(base_images_dir, filename), os.path.join(dataset_dir, str(symbol_id), filename))
                matched = True
                break
        if not matched:
            print(f"Missed base: {norm_fn}")

    # 2. Organize expansion images
    print("Organizing expansion images...")
    if os.path.exists(expansion_images_dir):
        expansion_files = [f for f in os.listdir(expansion_images_dir) if f.endswith('.jpg')]
        for filename in expansion_files:
            norm_fn = normalize(filename.replace('_alt.jpg', ''))
            matched = False
            for norm_name, symbol_id in name_to_id.items():
                if norm_fn == norm_name or norm_fn in norm_name or norm_name in norm_fn:
                    shutil.copy(os.path.join(expansion_images_dir, filename), os.path.join(dataset_dir, str(symbol_id), filename))
                    matched = True
                    break
            if not matched:
                print(f"Missed expansion: {norm_fn}")

    # Final count
    print(f"Refined organization complete. Classes with images: {len([d for d in os.listdir(dataset_dir) if len(os.listdir(os.path.join(dataset_dir, d))) > 0])}")

if __name__ == "__main__":
    refine_organization()
