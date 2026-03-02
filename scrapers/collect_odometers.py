import os
import json
import requests
from bs4 import BeautifulSoup

def collect_odometer_data():
    """
    Collects odometer image metadata and prepares for download.
    Note: Some datasets require manual intervention (login/license).
    """
    data_dir = 'data/odometers/raw'
    os.makedirs(data_dir, exist_ok=True)
    
    # Metadata for the collection
    collection_log = {
        "status": "In Progress",
        "sources": [
            {
                "id": "TRODO",
                "name": "TRODO Dataset",
                "url": "https://data.mendeley.com/datasets/9bsdtv2p3m/2",
                "notes": "Downloads as a ZIP. Contains 2389 images."
            },
            {
                "id": "Kaggle_Odometer",
                "name": "Kaggle Odometer",
                "url": "https://www.kaggle.com/datasets/craackmouse/odometer",
                "notes": "Requires Kaggle API or manual download."
            }
        ],
        "local_storage": data_dir
    }
    
    with open('data/odometers/collection_log.json', 'w') as f:
        json.dump(collection_log, f, indent=4)
        
    print(f"Collection log created at data/odometers/collection_log.json")
    print("Next step: Manual download of ZIP files into data/odometers/raw/ and extraction.")

if __name__ == "__main__":
    collect_odometer_data()
