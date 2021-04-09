from typing import TextIO, List

import requests
from pathlib import Path
import gzip
from .config import dvf_table_columns
from django.db import connection
from dvf.models import ValeursFoncieres

folder_path = str(Path.home())

def copy_csv(csv_file: TextIO,
             table_name: str,
             columns: List[str],
             delimiter: str,
             headers: bool,
             quote: str = None) -> None:
    column_names = ', '.join(columns)
    quote = quote or '"'
    cursor = connection.cursor()
    cmd = f"COPY {table_name} ({column_names})" \
          f"FROM STDIN " \
          f"WITH (" \
          f"FORMAT CSV, " \
          f"DELIMITER '{delimiter}', " \
          f"HEADER {headers}, " \
          f"QUOTE '{quote}')"
    cursor.copy_expert(cmd, csv_file)
    # connection.commit()

def build_url(year: int) -> str:
    return f'https://cadastre.data.gouv.fr/data/etalab-dvf/latest/csv/{year}/full.csv.gz'


def download_csv(url: str, folder_path: str) -> str:
    local_filename = f"{url.split('/')[-2]}_full.csv.gz"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(f"{folder_path}/{local_filename}", 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return local_filename


def import_gzipped_csv_to_db(gzipped_csv_file_path: str) -> None:
    with gzip.open(gzipped_csv_file_path, 'rb') as csv_file:
        copy_csv(
            csv_file=csv_file,
            table_name=ValeursFoncieres.objects.model._meta.db_table,
            columns=dvf_table_columns,
            delimiter=",",
            quote="",
            headers=True
        )


def import_data(year: int):
    url = build_url(year=year)
    local_filename = download_csv(url, folder_path)
    import_gzipped_csv_to_db(f"{folder_path}/{local_filename}")
