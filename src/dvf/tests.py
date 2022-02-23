from django.test import TestCase

from src.dvf.data.cities import get_city_from_code, get_city_from_slug, get_agent
from src.dvf.data.classes import Agent
from src.dvf.models import Commune

COMMUNE = {"code_commune": "34172", "nom_commune": "Montpellier", "slug": "montpellier-34080"}
AGENCY = {
    "code_commune": "34172",
    "picture_url": "https://estimer.com/static/images/icons/crown.svg",
    "agent": "Olivier Pourquier",
    "name": "estimer.com",
    "description": """Vous souhaitez obtenir une estimation précise de votre bien ?
                            Nous vous mettons en relation avec un agent immobilier local, expert sur votre secteur.""",
    "phone_number": "06.81.37.36.33",
    "email": "contact@estimer.com",
    "website_url": "Estimer.com",
}


class DvfTestCase(TestCase):
    fixtures = ["dvf_commune.json", "dvf_agent.json"]

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

    def test_agent_by_code_commune(self):
        agent = get_agent(code_commune=AGENCY["code_commune"])
        self.assertIsInstance(agent, Agent)
        self.assertEqual(agent.picture, AGENCY["picture_url"])
        self.assertEqual(agent.name, AGENCY["agent"])
        self.assertEqual(agent.agency, AGENCY["name"])
        self.assertEqual(agent.description, AGENCY["description"])
        self.assertEqual(agent.phone_number, AGENCY["phone_number"])
        self.assertEqual(agent.email, AGENCY["email"])
        self.assertEqual(agent.website_url, AGENCY["website_url"])
