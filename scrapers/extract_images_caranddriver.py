import requests
from bs4 import BeautifulSoup
import os
import json

url = "https://www.caranddriver.com/features/a26585375/dashboard-warning-lights-explained/"
# Car and Driver might require a User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

images = []
# On Car and Driver, symbols are often in <h2> or specialized containers
# They use a gallery format or individual sections
sections = soup.find_all(['h2', 'h3'])

for section in sections:
    name = section.get_text().strip()
    # Find the image associated with this header
    # Usually it's in a parent container or a sibling
    img = section.find_next('img')
    if img:
        img_url = None
        # Hearst sites (C&D) use data-src or just src
        for attr in ['data-src', 'src', 'srcset']:
            val = img.get(attr)
            if val and not val.startswith('data:image'):
                if attr == 'srcset':
                    img_url = val.split(',')[-1].split(' ')[0].strip()
                else:
                    img_url = val
                break
        
        if img_url:
            images.append({
                "name": name,
                "url": img_url
            })

os.makedirs('data', exist_ok=True)
with open('data/image_urls_expansion.json', 'w') as f:
    json.dump(images, f, indent=4)

print(f"Extracted {len(images)} expansion image URLs from Car and Driver.")
