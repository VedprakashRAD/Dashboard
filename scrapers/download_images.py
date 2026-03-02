import json
import requests
import os
from tqdm import tqdm

def download_images():
    with open('data/image_urls.json', 'r') as f:
        images = json.load(f)

    os.makedirs('data/images', exist_ok=True)

    print(f"Starting download of {len(images)} images...")
    
    # We only care about the first 89 as per the article
    for i, item in enumerate(tqdm(images[:89])):
        name = item['name'].split('. ', 1)[-1] if '. ' in item['name'] else item['name']
        filename = name.lower().replace('/', '_').replace(' ', '_').replace('(', '').replace(')', '').strip() + ".jpg"
        filepath = os.path.join('data/images', filename)
        
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
    download_images()
