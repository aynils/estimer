import requests
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CSV_DIR = BASE_DIR / 'dvf/aggregator'


def scrap_close_commune():
    path_csv_code_postal = CSV_DIR / 'estimer_public_dvf_commune.csv'  # Code Postal récupérer de la BDD Estimer.com (
    # dvf_commune)
    print(path_csv_code_postal)
    code_postal_df = pd.read_csv(path_csv_code_postal, usecols=["code_postal"])

    voisin = {}
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

            lst = []

            for i in a:
                if type(i) is str:
                    b = str(i)
                    lst.append([a[b]['nom_commune'], a[b]['code_postal'], a[b]['distance']])
                else:
                    lst.append([i['nom_commune'], i['code_postal'], i['distance']])

                y = 10
                for i in range(0, len(lst) - y):
                    lst.pop()
            print(lst)
            voisin[cp] = lst

    file_csv = open('commune_voisine.csv', 'w')
    for key, value in voisin.items():
        file_csv.write(str(key) + ';' + str(value) + '\n')
    file_csv.close()


def import_data():
    scrap_close_commune()
