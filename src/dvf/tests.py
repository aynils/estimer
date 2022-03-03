import datetime
from decimal import Decimal
from typing import Dict

import pandas as pd
from django.test import TestCase

from src.dvf.data.cities import (
    get_city_from_code,
    get_city_from_slug,
    get_agent,
    get_avg_m2_price_per_year,
    get_simple_sales,
    get_avg_m2_price_rooms,
)
from src.dvf.data.classes import Agent
from src.dvf.models import Commune

COMMUNE = {"code_commune": "34172", "nom_commune": "Montpellier", "slug": "montpellier-34080"}
AGENCIES = {
    "Saint-Jean-de-Védas": {
        "code_commune": "34270",
        "agency": "estimer.com",
        "picture": "https://estimer.com/static/images/icons/crown.svg",
        "name": "Olivier Pourquier",
        "description": """Vous représentez une agence et souhaitez obtenir plus de mandats à Saint-Jean-de-Védas ? Réservez votre
                annonce exclusive sur cette page.""",
        "phone_number": "06.81.37.36.33",
        "email": "contact@estimer.com",
        "website_url": "https://estimer.com",
        "short_url": "Estimer.com",
    },
    "montpellier": {
        "code_commune": "34172",
        "picture": "https://estimer.com/static/images/icons/crown.svg",
        "name": "Nabil Benaboura",
        "agency": "Helium Immobilier",
        "description": "Être la seule agence qui représente mon secteur est un réel plus pour ma visibilité et ma notoriété.",
        "phone_number": "0607265988",
        "email": "NabilBenaboura@HeliumImmobilier.com",
        "website_url": "https://www.heliumimmobilier.com/",
        "short_url": "heliumimmobilier.com",
    },
}


TODAY = datetime.date.today()
ONE_YEAR_AGO = datetime.date(year=TODAY.year - 1, month=1, day=1)


class DvfTestCase(TestCase):
    fixtures = ["agencies_agency.json", "dvf_commune.json", "dvf_valeursfoncieres.json"]

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
        agent = get_agent(code_commune=AGENCIES["montpellier"]["code_commune"])
        self.assertIsInstance(agent, Agent)
        self.assertEqual(agent.picture, AGENCIES["montpellier"]["picture"])
        self.assertEqual(agent.name, AGENCIES["montpellier"]["name"])
        self.assertEqual(agent.agency, AGENCIES["montpellier"]["agency"])
        self.assertEqual(agent.description, AGENCIES["montpellier"]["description"])
        self.assertEqual(agent.phone_number, AGENCIES["montpellier"]["phone_number"])
        self.assertEqual(agent.email, AGENCIES["montpellier"]["email"])
        self.assertEqual(agent.website_url, AGENCIES["montpellier"]["website_url"])
        self.assertEqual(agent.short_url, AGENCIES["montpellier"]["short_url"])

    def test_default_agent_by_code_commune(self):
        agent = get_agent(code_commune=AGENCIES["Saint-Jean-de-Védas"]["code_commune"])
        self.assertIsInstance(agent, Agent)
        self.assertEqual(agent.picture, AGENCIES["Saint-Jean-de-Védas"]["picture"])
        self.assertEqual(agent.name, AGENCIES["Saint-Jean-de-Védas"]["name"])
        self.assertEqual(agent.agency, AGENCIES["Saint-Jean-de-Védas"]["agency"])
        self.assertEqual(agent.description, AGENCIES["Saint-Jean-de-Védas"]["description"])
        self.assertEqual(agent.phone_number, AGENCIES["Saint-Jean-de-Védas"]["phone_number"])
        self.assertEqual(agent.email, AGENCIES["Saint-Jean-de-Védas"]["email"])
        self.assertEqual(agent.website_url, AGENCIES["Saint-Jean-de-Védas"]["website_url"])
        self.assertEqual(agent.short_url, AGENCIES["Saint-Jean-de-Védas"]["short_url"])

    def test_get_simple_sales(self):
        sales = get_simple_sales(
            code_commune=COMMUNE["code_commune"], types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO
        )
        self.assertIsInstance(sales, pd.DataFrame)
        self.assertEqual(len(sales), 1141)
        self.assertTrue(len(set(sales["id_mutation"])) == len(sales["id_mutation"]))
        self.assertSetEqual(set(sales["type_local"]), {"Maison", "Appartement"})
        # self.assertTrue(set(sales["date_mutation"]) < ONE_YEAR_AGO)

    def test_get_avg_m2_price_per_year(self):
        ventes = get_simple_sales(
            code_commune=COMMUNE["code_commune"], types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO
        )
        avg_price = get_avg_m2_price_per_year(types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO, ventes=ventes)
        self.assertIsInstance(avg_price, Dict)
        self.assertEqual(avg_price[2021], 3187.63)
        self.assertEqual(avg_price, {ONE_YEAR_AGO.year: 3187.63})

    def test_get_avg_m2_price_rooms(self):
        ventes = get_simple_sales(
            code_commune=COMMUNE["code_commune"], types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO
        )
        avg_price_per_room = get_avg_m2_price_rooms(
            types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO, ventes=ventes
        )
        self.assertIsInstance(avg_price_per_room, Dict)
        self.assertEqual(avg_price_per_room, {1: 3625, 2: 3267, 3: 3043, 4: 2916, 5: 3082, 6: 2836, 7: 3162, 8: 1193})
