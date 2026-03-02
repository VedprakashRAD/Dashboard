import requests
import os
from tqdm import tqdm

def collect_background():
    # Use a more reliable source or static URLs for non-dashboard/general car images
    # These are placeholder URLs from common stock repositories that represent "car interior" or "road"
    urls = [
        "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=640&q=80", # Car on road
        "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=640&q=80", # Car engine
        "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=640&q=80", # Steering wheel
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=640&q=80", # Dashboard no icons
        "https://images.unsplash.com/photo-1517672791834-032954a7c50a?w=640&q=80", # Car seat
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=640&q=80", # Car wheel
    ]
    
    os.makedirs('data/background_images', exist_ok=True)
    
    count = 0
    for i, url in enumerate(urls):
        try:
            print(f"Downloading background image {i+1}...")
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                with open(f'data/background_images/bg_{i}.jpg', 'wb') as f:
                    f.write(response.content)
                count += 1
        except Exception as e:
            print(f"Error downloading {url}: {e}")

    print(f"Collected {count} fallback background images.")

if __name__ == "__main__":
    collect_background()
