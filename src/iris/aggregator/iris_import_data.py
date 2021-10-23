import sys
import pandas as pd
from pyproj import CRS
import fiona

# Les champs issus fichier shp IGN
IGN_FIELDS = ("INSEE_COM", "NOM_COM", "IRIS", "CODE_IRIS", "NOM_IRIS", "TYP_IRIS")
IGN_SRID = "epsg:2154"  # Lambert 93


def lire_fichier_ign():
    print("lecture du fichier shapefile IGN")
    with fiona.open("/home/cink/Bureau/DEV/estimer/src/iris/data/CONTOURS-IRIS.shp") as reader:
        properties = reader.meta["schema"]["properties"]
        crs = CRS.from_wkt(reader.meta["crs_wkt"])
        srid = "epsg:{}".format(crs.to_epsg())
        # on vérifie que le nom des champs sont conformes
        if tuple(properties.keys()) != IGN_FIELDS:
            print("Les champs IGN ont changé.")
            print("Champs IGN demandés : %s", IGN_FIELDS)
            print("Champs IGN trouvés : %s", tuple(properties.keys()))
            sys.exit(1)

        # on vérifie que le système de projection est lambert 93
        if srid != IGN_SRID:
            print("Le système de projection devrait être '%s' et non '%s'", IGN_SRID, srid)
            sys.exit(1)

        data = [row["properties"] for row in reader]
        pandaframetocsv = pd.DataFrame(data)
        return pandaframetocsv.to_csv(r'/home/cink/Bureau/DEV/estimer/src/iris/data/dataframetocsv.csv')
