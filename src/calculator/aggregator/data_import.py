import requests
import os.path
import zipfile
from pathlib import Path

folder_path = str(Path.home())


def build_url() -> str:
    return f"https://www.insee.fr/fr/statistiques/fichier/5650720/base-ic-evol-struct-pop-2018_csv.zip"


def download_zip(url: str, folder_path: str) -> str:
    local_filename = f"{url.split('/')[-1]}"
    if not os.path.exists(f"{folder_path}/{local_filename}"):
        print("Downloading files ...")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(f"{folder_path}/{local_filename}", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    else:
        print("File already existing. Skip download")

    return local_filename


def extract_zip():
    url = build_url()
    local_filename = download_zip(url, folder_path)
    file_path = f"{folder_path}/{local_filename}"
    with zipfile.ZipFile(f"{file_path}", "r") as zip_ref:
        zip_ref.extractall(path=f"{folder_path}")

    return ""
