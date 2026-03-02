import requests
from bs4 import BeautifulSoup
import os
import json

def scrape_halfords():
    url = "https://www.halfords.com/motoring/advice/car-warning-lights-what-do-they-mean.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"Scraping Halfords: {url}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    images = []
    # Halfords structure often uses h3/h4 for names and img nearby
    sections = soup.find_all(['h3', 'h4'])
    
    for section in sections:
        name = section.get_text().strip()
        if len(name) < 3: continue
        
        # Find the image - often inside a picture or nearby div
        parent = section.parent
        img = parent.find('img')
        if not img:
            img = section.find_next('img')
            
        if img:
            img_url = None
            for attr in ['data-src', 'src', 'srcset']:
                val = img.get(attr)
                if val and not val.startswith('data:image'):
                    if attr == 'srcset':
                        img_url = val.split(',')[-1].split(' ')[0].strip()
                    elif val.startswith('/'):
                        img_url = "https://www.halfords.com" + val
                    else:
                        img_url = val
                    break
            
            if img_url:
                images.append({
                    "name": name,
                    "url": img_url
                })
    
    output_path = 'data/image_urls_halfords.json'
    with open(output_path, 'w') as f:
        json.dump(images, f, indent=4)
    
    print(f"Extracted {len(images)} symbol URLs from Halfords.")

if __name__ == "__main__":
    scrape_halfords()
