import os
import requests
import pandas as pd
from serpapi import GoogleSearch
from dotenv import load_dotenv
load_dotenv()

def upload_image(image_path):
    """Upload an image to ImgBB and return the URL."""
    try:
        with open(image_path, "rb") as image_file:
            response = requests.post(
                "https://api.imgbb.com/1/upload",
                files={"image": image_file},
                params={"key": os.getenv('IMGBB_API_KEY')}
            )
        response.raise_for_status()
        return response.json().get("data", {}).get("url", "")
    except Exception as e:
        print(f"Image upload failed: {e}")
        return None

def google_lens_search(image_url):
    """Perform a Google Lens search and return the results."""
    try:
        search = GoogleSearch({
            "engine": "google_lens",
            "url": image_url,
            "no_cache": "true",
            "api_key": os.getenv('SERPAPI_KEY')
        })
        results = search.get_dict()
        return [match.get("thumbnail") for match in results.get("visual_matches", [])[:10]], \
               [match.get("link") for match in results.get("visual_matches", [])[:10]]
    except Exception as e:
        print(f"Google Lens search failed: {e}")
        return [], []

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
            else:
                thumbnails.append("Upload failed")
                links.append("")

    df = pd.DataFrame({
        "Thumbnails": thumbnails,
        "Links": links
    })
    df.to_excel('results.xlsx', index=False)
    print("All images processed and results are saved to results.xlsx.")

process_images(os.getenv('FOLDER_PATH'))
