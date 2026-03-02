import requests
from bs4 import BeautifulSoup
import os
import json

def scrape_rac():
    url = "https://www.rac.co.uk/drive/advice/know-how/dashboard-warning-lights/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"Scraping RAC: {url}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    images = []
    # RAC uses h3 for symbol names and usually the image is very close
    sections = soup.find_all('h3')
    
    for h3 in sections:
        name = h3.get_text().strip()
        # Find the image in the parent or siblings
        parent = h3.parent
        img = parent.find('img')
        
        if not img:
            # Try next sibling
            img = h3.find_next('img')
            
        if img:
            img_url = None
            for attr in ['data-src', 'src', 'data-original-src']:
                val = img.get(attr)
                if val and not val.startswith('data:image'):
                    if val.startswith('/'):
                        img_url = "https://www.rac.co.uk" + val
                    else:
                        img_url = val
                    break
            
            if img_url:
                images.append({
                    "name": name,
                    "url": img_url
                })
    
    output_path = 'data/image_urls_rac.json'
    with open(output_path, 'w') as f:
        json.dump(images, f, indent=4)
    
    print(f"Extracted {len(images)} symbol URLs from RAC.")

if __name__ == "__main__":
    scrape_rac()
