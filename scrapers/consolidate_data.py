import json
import os
import requests
from tqdm import tqdm
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def download_image(url, filepath):
    if os.path.exists(filepath):
        return True
    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
    except:
        pass
    return False

def consolidate_and_download():
    # Load 89 standard symbols
    with open('data/symbols_data.json', 'r') as f:
        standard_symbols = json.load(f)
    
    id_to_norm_name = {str(s['id']): s['name'].lower().replace(' ', '_').strip() for s in standard_symbols}
    id_to_real_name = {str(s['id']): s['name'] for s in standard_symbols}

    # Consolidated output dir for symbols
    # We will put them in data/dataset/{id}/raw_{source}_{index}.jpg
    os.makedirs('data/dataset', exist_ok=True)
    for sid in id_to_norm_name.keys():
        os.makedirs(os.path.join('data/dataset', sid), exist_ok=True)

    sources = {
        "mechanicbase": "data/image_urls.json",
        "caranddriver": "data/image_urls_expansion.json",
        "rac": "data/image_urls_rac.json",
        "halfords": "data/image_urls_halfords.json",
        "dashboardsymbols": "data/image_urls_dashboardsymbols.json"
    }

    counts = {sid: 0 for sid in id_to_norm_name.keys()}

    for source_name, source_file in sources.items():
        if not os.path.exists(source_file):
            print(f"Skipping {source_name}, file not found.")
            continue
            
        print(f"Processing {source_name}...")
        with open(source_file, 'r') as f:
            data = json.load(f)
            
        for i, item in enumerate(tqdm(data)):
            name = item['name'].lower()
            url = item['url']
            if not url.startswith('http'): continue
            
            # Skip common non-symbol icons
            if any(x in name for x in ['visa', 'mastercard', 'paypal', 'apple pay', 'google pay']):
                continue
            
            # Find best match in 89 symbols
            best_id = None
            highest_score = 0
            
            # 1. Exact or very close match
            for sid, sname in id_to_norm_name.items():
                # Check normalized name match
                score = similar(name, id_to_real_name[sid])
                
                # Boost if keywords match specifically
                if id_to_norm_name[sid] in name.replace(' ', '_'):
                    score += 0.2
                    
                if score > highest_score:
                    highest_score = score
                    best_id = sid
            
            # Threshold for matching - lowered slightly for expansion sources
            threshold = 0.55 if source_name != "mechanicbase" else 0.8
            if highest_score > threshold:
                filename = f"ext_{source_name}_{i}.jpg"
                filepath = os.path.join('data/dataset', best_id, filename)
                if download_image(url, filepath):
                    counts[best_id] += 1

    print("\nDownload Summary:")
    for sid, count in counts.items():
        if count > 0:
            print(f"ID {sid} ({id_to_real_name[sid]}): {count} images added")

if __name__ == "__main__":
    consolidate_and_download()
