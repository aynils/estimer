import requests
import pandas as pd
from pathlib import Path

from src.dvf.models import CommuneVoisine

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CSV_DIR = BASE_DIR / 'dvf/aggregator'
path_csv_out_file = CSV_DIR / 'commune_voisine.csv'


def scrap_close_commune():
    path_csv_code_postal = CSV_DIR / 'liste_code_postal_test.csv'  # Code Postal récupérer de la BDD Estimer.com
    code_postal_df = pd.read_csv(path_csv_code_postal, usecols=["code_postal"])
    for codepostal in code_postal_df['code_postal']:
        if codepostal <= 9999:
            cp = '0' + str(codepostal)
        else:
            cp = str(codepostal)
        print(cp)
        rayon = '50'
        myurl = 'https://www.villes-voisines.fr/getcp.php?cp=' + cp + '&rayon=' + rayon
        r = requests.get(myurl)
        if (r.json()) is not None:
            a = r.json()
            commune_voisines = []
            if type(a) == list:
                for i in a:
                    commune_voisine = CommuneVoisine(code_postal_a=cp, code_postal_b=i['code_postal'], distance=i['distance'])
                    commune_voisines.append(commune_voisine)
            else:
                filtered_json = {commune.get('code_postal'): commune.get('distance') for commune in a.values()}
                for key, value in filtered_json.items():
                    if key or value:
                        commune_voisine = CommuneVoisine(code_postal_a=cp, code_postal_b=key, distance=value)
                        commune_voisines.append(commune_voisine)

            CommuneVoisine.objects.bulk_create(commune_voisines)
