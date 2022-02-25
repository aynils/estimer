from django.db.models import QuerySet
from django.test import TestCase

from src.agencies.data.calculator import get_cities_not_owned_by_agencies

COMMUNE = {
    "code_postal": "34430",
    "code_commune": "34270",
    "nom_commune": "Saint-Jean-de-Védas",
    "slug": "saint-jean-de-vedas-34430",
    "code_departement": "34",
    "agency_id": None,
}


class AgenciesTestCase(TestCase):
    fixtures = ["dvf_commune.json", "agencies_agency.json"]

    def test_cities_not_owned_by_agencies(self):
        cities = get_cities_not_owned_by_agencies(code_departement=COMMUNE["code_departement"])
        self.assertIsInstance(cities, QuerySet)
        self.assertEqual(len(cities), 1)
        self.assertEqual(cities[0]["code_postal"], COMMUNE["code_postal"])
        self.assertEqual(cities[0]["nom_commune"], COMMUNE["nom_commune"])
        self.assertEqual(cities[0]["code_commune"], COMMUNE["code_commune"])
