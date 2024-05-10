import os
import requests
import pandas as pd
from serpapi import GoogleSearch
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
MAX_RESULTS = 20

def upload_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            response = requests.post(
                "https://api.imgbb.com/1/upload",
                files={"image": image_file},
                params={"key": os.getenv('IMGBB_API_KEY')},
                timeout=10
            )
        response.raise_for_status()
        return response.json().get("data", {}).get("url", "")
    except requests.exceptions.RequestException as e:
        print(f"Network or request issue: {e}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
    return None

def google_lens_search(image_url):
    try:
        search = GoogleSearch({
            "engine": "google_lens",
            "url": image_url,
            "no_cache": "true",
            "api_key": os.getenv('SERPAPI_KEY')
        })
        results = search.get_dict()
        thumbnails, links = zip(*[(match.get("thumbnail"), match.get("link")) for match in results.get("visual_matches", [])[:MAX_RESULTS]])
        return list(thumbnails), list(links)
    except Exception as e:
        print(f"Search API error: {e}")
        return [], []

def process_images(folder_path):
    data = []
    for filename in tqdm(os.listdir(folder_path)):
        if filename.lower().endswith(SUPPORTED_FORMATS):
            print(f"Processing {filename}...")
            image_url = upload_image(os.path.join(folder_path, filename))
            if image_url:
                thumbnails, links = google_lens_search(image_url)
                data.append([filename] + thumbnails + links)
            else:
                data.append([filename] + ["Upload failed"] * (2 * MAX_RESULTS))

    column_names = ['Filename'] + [f"Thumbnail {i+1}" for i in range(MAX_RESULTS)] + [f"Link {i+1}" for i in range(MAX_RESULTS)]
    df = pd.DataFrame(data, columns=column_names)
    df.to_excel('results.xlsx', index=False)
    print("All images processed and results are saved to results.xlsx.")

process_images(os.getenv('FOLDER_PATH'))
