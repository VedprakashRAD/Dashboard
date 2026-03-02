import json
import requests
import os
from tqdm import tqdm

def download_expansion():
    with open('data/image_urls_expansion.json', 'r') as f:
        images = json.load(f)

    os.makedirs('data/images/expansion', exist_ok=True)

    print(f"Starting download of {len(images)} expansion images...")
    
    for item in tqdm(images):
        name = item['name'].strip()
        # Skip generic icons
        if name in ["Jump to:", "For Sale Near You", "Essential Reads: Stories and Features"]:
            continue
            
        filename = name.lower().replace('/', '_').replace(' ', '_').replace(',', '').replace(':', '').replace('-', '_').replace('+', '_').strip() + "_alt.jpg"
        filepath = os.path.join('data/images/expansion', filename)
        
        try:
            response = requests.get(item['url'], stream=True, timeout=10)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
            else:
                print(f"Failed to download {name}: {response.status_code}")
        except Exception as e:
            print(f"Error downloading {name}: {e}")

if __name__ == "__main__":
    download_expansion()
