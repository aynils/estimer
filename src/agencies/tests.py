from typing import List

from django.db.models import QuerySet
from django.test import TestCase

from src.agencies.data.calculator import (
    get_cities_not_owned_by_agencies,
    add_population_to_cities,
    add_pricing_to_cities,
    get_cities_with_pricing,
)

COMMUNE = {
    "code_postal": "34430",
    "code_commune": "34270",
    "nom_commune": "Saint-Jean-de-Védas",
    "slug": "saint-jean-de-vedas-34430",
    "code_departement": "34",
    "agency_id": None,
}


class AgenciesTestCase(TestCase):
    fixtures = ["dvf_commune.json", "agencies_agency.json", "population_populationstat.json", "agencies_pricing.json"]

    def test_cities_not_owned_by_agencies(self):
        cities = get_cities_not_owned_by_agencies(code_departement=COMMUNE["code_departement"])
        self.assertIsInstance(cities, QuerySet)
        self.assertEqual(len(cities), 1)
        self.assertEqual(cities[0]["code_postal"], COMMUNE["code_postal"])
        self.assertEqual(cities[0]["nom_commune"], COMMUNE["nom_commune"])
        self.assertEqual(cities[0]["code_commune"], COMMUNE["code_commune"])

    def test_add_population_to_cities(self):
        cities = get_cities_not_owned_by_agencies(code_departement=COMMUNE["code_departement"])
        cities_with_population = add_population_to_cities(cities=cities)
        self.assertIsInstance(cities_with_population, List)
        self.assertEqual(len(cities_with_population), 1)
        self.assertEqual(cities_with_population[0]["code_postal"], COMMUNE["code_postal"])
        self.assertEqual(cities_with_population[0]["nom_commune"], COMMUNE["nom_commune"])
        self.assertEqual(cities_with_population[0]["total_population"], 4701.41909758321)

    def test_add_pricing_to_cities(self):
        cities = get_cities_not_owned_by_agencies(code_departement=COMMUNE["code_departement"])
        cities_with_population = add_population_to_cities(cities=cities)
        cities_with_pop_and_pricing = add_pricing_to_cities(cities=cities_with_population)
        self.assertIsInstance(cities_with_pop_and_pricing, List)
        self.assertEqual(len(cities_with_pop_and_pricing), 1)
        self.assertEqual(cities_with_pop_and_pricing[0]["code_postal"], COMMUNE["code_postal"])
        self.assertEqual(cities_with_pop_and_pricing[0]["nom_commune"], COMMUNE["nom_commune"])
        self.assertEqual(cities_with_pop_and_pricing[0]["pricing"], 50.0)

    def test_get_cities_with_pricing(self):
        cities_with_pricing = get_cities_with_pricing(code_departement=COMMUNE["code_departement"])
        self.assertIsInstance(cities_with_pricing, List)
        self.assertEqual(len(cities_with_pricing), 1)
        self.assertEqual(cities_with_pricing[0]["code_postal"], COMMUNE["code_postal"])
        self.assertEqual(cities_with_pricing[0]["nom_commune"], COMMUNE["nom_commune"])
        self.assertEqual(cities_with_pricing[0]["pricing"], 50.0)
