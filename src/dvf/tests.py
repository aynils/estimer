from django.test import TestCase

from src.dvf.data.cities import get_city_from_code, get_city_from_slug
from src.dvf.models import Commune

COMMUNE = {"code_commune": "34172", "nom_commune": "Montpellier", "slug": "montpellier-34080"}


class DvfTestCase(TestCase):
    fixtures = ["dvf_commune.json"]

    def test_commune_by_code_commune(self):
        commune = get_city_from_code(code=COMMUNE["code_commune"])
        self.assertIsInstance(commune, Commune)
        self.assertEqual(commune.code_commune, COMMUNE["code_commune"])
        self.assertEqual(commune.slug, COMMUNE["slug"])

    def test_commune_by_slug(self):
        commune = get_city_from_slug(slug=COMMUNE["slug"])
        self.assertIsInstance(commune, Commune)
        self.assertEqual(commune.code_commune, COMMUNE["code_commune"])
        self.assertEqual(commune.slug, COMMUNE["slug"])
