from google_images_search import GoogleImagesSearch

gis = GoogleImagesSearch('AIzaSyDMNHmTDePsJV7gjktX8Z7ak20OoHlhob4', '24b94c30a21744459')

_search_params = {
    'q': 'ahinur-baldo-pirinc',
    'num': 3,
    'safe': 'off'
}

gis.search(search_params=_search_params, path_to_dir='/Users/zackhatlen/Desktop/test/')