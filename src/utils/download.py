from urllib.parse import urlparse

import requests
from pathlib import Path


def download_file_from_url(url, path):
    """Download file from url into preferred directory"""

    file_path = path / Path(urlparse(url).path).name

    if file_path.exists():
        print(file_path, 'already exists')
        return file_path

    path.mkdir(parents=True, exist_ok=True)

    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            f.write(response.raw.read())
            print(file_path, 'downloaded')

    return file_path
