import os
import requests
import pandas as pd
from serpapi import GoogleSearch

def upload_image(image_path):
    """Upload an image to ImgBB and return the URL."""
    response = requests.post(
        "https://api.imgbb.com/1/upload",
        files={"image": open(image_path, "rb")},
        params={"key": "fe4095abd2b2d313d039c4d7e28fb628"}
    )
    return response.json().get("data", {}).get("url", "")

def google_lens_search(image_url):
    """Perform a Google Lens search and return the results."""
    search = GoogleSearch({
        "engine": "google_lens",
        "url": image_url,
        "no_cache": "true",
        "api_key": "19d3c31622298ef05734523b5be56d83edbb2db22680cd2e1c1e8b8fc1f85c66"
    })
    results = search.get_dict()
    return [match.get("thumbnail") for match in results.get("visual_matches", [])[:10]], \
           [match.get("link") for match in results.get("visual_matches", [])[:10]]

def process_images(folder_path):
    """Process images in the given folder and save the results to an Excel file."""
    thumbnails, links = [], []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp' )):
            print(f"Processing {filename}...")
            image_url = upload_image(os.path.join(folder_path, filename))
            if image_url:
                th, ln = google_lens_search(image_url)
                thumbnails.append(th)
                links.append(", ".join(ln))
    
    df = pd.DataFrame({
        "Thumbnails": thumbnails,
        "Links": links
    })
    df.to_excel('results.xlsx', index=False)

FOLDER_PATH = '/Users/zackhatlen/Desktop/test/'
process_images(FOLDER_PATH)