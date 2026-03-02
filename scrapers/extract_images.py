import requests
from bs4 import BeautifulSoup
import os
import json

url = "https://mechanicbase.com/engine/dashboard-symbols/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

images = []
# Find all column blocks which contain both the image and the header
columns = soup.find_all('div', class_='wp-block-column')

for column in columns:
    h3 = column.find('h3')
    img = column.find('img')
    
    if h3 and img:
        name = h3.get_text().strip()
        # Priority for real image URLs over placeholders
        img_url = None
        
        # Check common lazy loading attributes
        for attr in ['data-lazy-src', 'data-src', 'srcset', 'src']:
            val = img.get(attr)
            if val and not val.startswith('data:image'):
                if attr == 'srcset':
                    # Get the largest image from srcset
                    img_url = val.split(',')[-1].split(' ')[0].strip()
                else:
                    img_url = val
                break
        
        if img_url:
            images.append({
                "name": name,
                "url": img_url
            })

with open('data/image_urls.json', 'w') as f:
    json.dump(images, f, indent=4)

print(f"Extracted {len(images)} image URLs.")
