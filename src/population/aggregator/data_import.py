import requests
import os.path
import gzip
import logging

from typing import TextIO, List
from django.db import connection
from population.models import PopulationStat

from pathlib import Path
from .config import calculator_table_columns

logger = logging.getLogger(__name__)
folder_path = str(Path.home())


def copy_csv(
    csv_file: TextIO, table_name: str, columns: List[str], delimiter: str, headers: bool, quote: str = None
) -> None:
    column_names = ", ".join(columns)
    quote = quote or '"'
    cursor = connection.cursor()
    cmd = (
        f"COPY {table_name} ({column_names})"
        f"FROM STDIN "
        f"WITH ("
        f"FORMAT CSV, "
        f"DELIMITER '{delimiter}', "
        f"HEADER {headers}, "
        f"QUOTE '{quote}')"
    )
    cursor.copy_expert(cmd, csv_file)
    # connection.commit()
    return ""


def build_url() -> str:
    return f"https://www.insee.fr/fr/statistiques/fichier/5650720/base-ic-evol-struct-pop-2018_csv.zip"


def download_csv(url: str, folder_path: str) -> str:
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


def import_gzipped_csv_to_db(gzipped_csv_file_path: str) -> None:
    print("Import data from zip file")
    with gzip.open(gzipped_csv_file_path, "rb") as csv_file:
        copy_csv(
            csv_file=csv_file,
            table_name=PopulationStat.objects.model._meta.db_table,
            columns=calculator_table_columns,
            delimiter=",",
            quote="",
            headers=True,
        )
    return ""


def import_data():
    url = build_url()
    local_filename = download_csv(url, folder_path)
    file_path = f"{folder_path}/{local_filename}"
    import_gzipped_csv_to_db(gzipped_csv_file_path=file_path)
    return ""
