import logging

from django.contrib.gis.utils import LayerMapping

from iris.models import IRIS

logger = logging.getLogger(__name__)

IGN_SRID = "epsg:2154"  # Lambert 93


# TODO: add script to download this file from the server
SHP_INPUT_PATH = "/Users/seraphinvandegar/Downloads/CONTOURS-IRIS_2-1__SHP__FRA_2018-01-01/CONTOURS-IRIS/1_DONNEES_LIVRAISON_2018-07-00057/CONTOURS-IRIS_2-1_SHP_LAMB93_FXX-2018"


def import_data():
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
