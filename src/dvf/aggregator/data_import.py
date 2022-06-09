import gzip
import os.path
from pathlib import Path
from typing import TextIO, List

import requests
from django.db import connection
from slugify import slugify

from src.dvf.models import ValeursFoncieres, Commune
from .config import dvf_table_columns

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


def build_url(year: int) -> str:
    return f"https://files.data.gouv.fr/geo-dvf/latest/csv/{year}/full.csv.gz"


def download_csv(url: str, folder_path: str) -> str:
    local_filename = f"{url.split('/')[-2]}_full.csv.gz"
    if not os.path.exists(f"{folder_path}/{local_filename}"):
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
            table_name=ValeursFoncieres.objects.model._meta.db_table,
            columns=dvf_table_columns,
            delimiter=",",
            quote="",
            headers=True,
        )


def delete_existing_data(year: int) -> None:
    print("delete existing data")
    # TODO: fix this function
    ValeursFoncieres.objects.raw(
        f"""
    DELETE FROM dvf_valeursfoncieres
    WHERE EXTRACT(year FROM dvf_valeursfoncieres.date_mutation) = {int(year)}
    ;"""
    )


def create_communes():
    print("create communes")
    rows = ValeursFoncieres.objects.order_by("code_commune").distinct("code_commune").all()
    communes = [
        Commune(
            code_commune=row.code_commune,
            code_postal=row.code_postal,
            nom_commune=row.nom_commune,
            code_departement=row.code_departement,
            slug=slugify(f"{row.nom_commune}-{row.code_postal}"),
        )
        for row in rows
    ]
    Commune.objects.bulk_create(communes, ignore_conflicts=True)


def import_data(year: int):
    url = build_url(year=year)
    local_filename = download_csv(url, folder_path)
    file_path = f"{folder_path}/{local_filename}"
    delete_existing_data(year=year)
    import_gzipped_csv_to_db(gzipped_csv_file_path=file_path)
    create_communes()
