import requests
import os.path
import logging
import zipfile

import pandas as pd
from pathlib import Path
from django.db import connection
from sqlalchemy import create_engine

from population.models import PopulationStat

logger = logging.getLogger(__name__)
folder_path = str(Path.home())


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


def extract_zip():
    url = build_url()
    local_filename = download_csv(url, folder_path)
    file_path = f"{folder_path}/{local_filename}"
    with zipfile.ZipFile(f"{file_path}", "r") as zip_ref:
        zip_ref.extractall(path=f"{folder_path}/population_data")
    return ""


def csv_to_dataframe():
    path_csv = f"{folder_path}/population_data/base-ic-evol-struct-pop-2018.CSV"
    population_df = pd.read_csv(
        f"{path_csv}",
        sep=";",
        usecols=[
            "IRIS",
            "COM",
            "TYP_IRIS",
            "MODIF_IRIS",
            "LAB_IRIS",
            "P18_POP",
            "P18_POP0002",
            "P18_POP0305",
            "P18_POP0610",
            "P18_POP1117",
            "P18_POP1824",
            "P18_POP2539",
            "P18_POP4054",
            "P18_POP5564",
            "P18_POP6579",
            "P18_POP80P",
            "P18_POP0014",
            "P18_POP1529",
            "P18_POP3044",
            "P18_POP4559",
            "P18_POP6074",
            "P18_POP75P",
            "P18_POP0019",
            "P18_POP2064",
            "P18_POP65P",
        ],
    )

    population_df.rename(
        columns={
            "IRIS": "iris",
            "COM": "code_commune",
            "TYP_IRIS": "type_iris",
            "MODIF_IRIS": "modification_iris",
            "LAB_IRIS": "label_iris",
            "P18_POP": "total_population",
            "P18_POP0002": "population_0_2",
            "P18_POP0305": "population_3_5",
            "P18_POP0610": "population_6_10",
            "P18_POP1117": "population_11_17",
            "P18_POP1824": "population_18_24",
            "P18_POP2539": "population_25_39",
            "P18_POP4054": "population_40_54",
            "P18_POP5564": "population_55_64",
            "P18_POP6579": "population_65_79",
            "P18_POP80P": "population_80_more",
            "P18_POP0014": "population_0_14",
            "P18_POP1529": "population_15_29",
            "P18_POP3044": "population_30_44",
            "P18_POP4559": "population_45_59",
            "P18_POP6074": "population_60_74",
            "P18_POP75P": "population_75_more",
            "P18_POP0019": "population_0_19",
            "P18_POP2064": "population_20_64",
            "P18_POP65P": "population_65_more",
        },
        inplace=True,
    )
    return population_df


def dataframe_to_sql():

    user = connection.settings_dict["USER"]
    password = connection.settings_dict["PASSWORD"]
    database_name = connection.settings_dict["NAME"]
    host = connection.settings_dict["HOST"]
    port = connection.settings_dict["PORT"]

    population_df = csv_to_dataframe()

    database_url = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"

    engine = create_engine(database_url, echo=False)
    population_df.to_sql(PopulationStat._meta.db_table, con=engine, index=True, if_exists="replace")
    return ""


def import_data():
    url = build_url()
    download_csv(url=url, folder_path=folder_path)
    extract_zip()
    csv_to_dataframe()
    dataframe_to_sql()
    return ""
