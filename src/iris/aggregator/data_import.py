import logging

from django.contrib.gis.utils import LayerMapping

from iris.models import IRIS

import requests
import os.path
from pathlib import Path
import py7zr

logger = logging.getLogger(__name__)

IGN_SRID = "epsg:2154"  # Lambert 93

folder_path = str(Path.home())


def build_url(year: int) -> str:
    return f"http://data.cquest.org/ign/contours-iris/CONTOURS-IRIS_2-1__SHP__FRA_{year}-01-01.7z"


def download_shp(url: str, folder_path: str) -> str:
    local_filename = f"{url.split('/')[-1]}"
    if not os.path.exists(f"{folder_path}/{local_filename}"):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(f"{folder_path}/{local_filename}", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    else:
        print("File already existing. Skip download")

    return local_filename


def extract_zip(year: int):
    url = build_url(year=year)
    local_filename = download_shp(url, folder_path)
    file_path = f"{folder_path}/{local_filename}"
    with py7zr.SevenZipFile(f"{file_path}", "r") as archive:
        archive.extractall(path=f"{folder_path}")


# TODO: add script to download this file from the server
SHP_INPUT_PATH = (
    "/home/cink/Téléchargements/CONTOURS-IRIS_2-1__SHP__FRA_2020-01-01/"
    "CONTOURS-IRIS/1_DONNEES_LIVRAISON_2020-12-00282/"
    "CONTOURS-IRIS_2-1_SHP_LAMB93_FXX-2020"
)


def import_data(year=2021):
    logger.info("Reading IGN shapefile")

    mapping = {
        "insee_commune": "INSEE_COM",
        "nom_commune": "NOM_COM",
        "iris": "IRIS",
        "code_iris": "CODE_IRIS",
        "nom_iris": "NOM_IRIS",
        "type_iris": "TYP_IRIS",
        "geometry": "MULTIPOLYGON",
    }

    lm = LayerMapping(IRIS, SHP_INPUT_PATH, mapping, transform=False, encoding="utf-8")

    lm.save(strict=True, verbose=True)
