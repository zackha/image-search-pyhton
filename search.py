import os
import requests
from serpapi import GoogleSearch

def upload_image_to_imgbb(image_path, imgbb_key):
    url = "https://api.imgbb.com/1/upload"
    with open(image_path, 'rb') as file:
        files = {"image": file}
        params = {"key": imgbb_key}
        response = requests.post(url, files=files, params=params)
        data = response.json()
        return data.get("data", {}).get("url")

def search_image_on_google_lens(image_url, serpapi_key):
    params = {
        "engine": "google_lens",
        "url": image_url,
        "no_cache": "true",
        "api_key": serpapi_key,
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results

def process_folder(folder_path, imgbb_key, serpapi_key):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
            image_path = os.path.join(folder_path, filename)
            print(f"Processing {filename}...")
            try:
                uploaded_image_url = upload_image_to_imgbb(image_path, imgbb_key)
                if uploaded_image_url:
                    results = search_image_on_google_lens(uploaded_image_url, serpapi_key)
                    if results.get('search_metadata', {}).get('status') == 'Success' and results.get('visual_matches'):
                        first_match = results['visual_matches'][0]  # İlk eşleşmeyi al
                        link = first_match.get('link')
                        image = first_match.get('thumbnail')  # Thumbnail resim linki
                        if link:
                            print("Link:", link)
                        if image:
                            print("Image:", image)
                    else:
                        print("No results found.")
                else:
                    print("Failed to upload image.")
            except Exception as e:
                print(f"An error occurred: {e}")

# Kullanıcı bu bilgileri doğru şekilde sağlamalıdır.
IMG_API_KEY = 'fe4095abd2b2d313d039c4d7e28fb628'
SERP_API_KEY = '19d3c31622298ef05734523b5be56d83edbb2db22680cd2e1c1e8b8fc1f85c66'
FOLDER_PATH = '/Users/zackhatlen/Desktop/test/'

process_folder(FOLDER_PATH, IMG_API_KEY, SERP_API_KEY)
