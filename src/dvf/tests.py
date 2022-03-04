import datetime
from decimal import Decimal
from typing import Dict, List

import pandas as pd
from django.test import TestCase

from src.dvf.data.cities import (
    get_city_from_code,
    get_city_from_slug,
    get_agent,
    get_avg_m2_price_per_year,
    get_simple_sales,
    get_avg_m2_price_rooms,
    get_avg_m2_price_street,
    get_last_sales,
    get_city_data,
    get_neighbourhoods_data,
)
from src.dvf.data.classes import Agent, MedianM2PriceRoom, CityData, MedianM2Price
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
FIVE_YEARS_AGO = datetime.date(year=TODAY.year - 5, month=1, day=1)


class DvfTestCase(TestCase):
    fixtures = [
        "agencies_agency.json",
        "dvf_commune.json",
        "dvf_valeursfoncieres.json",
        "iris_iris.json",
        "dvf_mutationiris.json",
    ]

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
        self.assertTrue(all(sales["date_mutation"] >= ONE_YEAR_AGO))

    def test_get_avg_m2_price_per_year(self):
        ventes = get_simple_sales(
            code_commune=COMMUNE["code_commune"], types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO
        )
        avg_price = get_avg_m2_price_per_year(types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO, ventes=ventes)
        self.assertIsInstance(avg_price, Dict)
        self.assertEqual(avg_price[2021], 3187.63)
        self.assertEqual(avg_price, {ONE_YEAR_AGO.year: 3187.63})
        self.assertEqual(len(avg_price), 1)

    def test_get_avg_m2_price_rooms(self):
        ventes = get_simple_sales(
            code_commune=COMMUNE["code_commune"], types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO
        )
        avg_price_per_room = get_avg_m2_price_rooms(
            types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO, ventes=ventes
        )
        self.assertIsInstance(avg_price_per_room, Dict)
        self.assertEqual(avg_price_per_room, {1: 3625, 2: 3267, 3: 3043, 4: 2916, 5: 3082, 6: 2836, 7: 3162, 8: 1193})
        self.assertEqual(len(avg_price_per_room), 8)

    def test_get_avg_m2_price_street(self):
        ventes = get_simple_sales(
            code_commune=COMMUNE["code_commune"], types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO
        )
        avg_price_per_street = get_avg_m2_price_street(limit=5, ascending=True, ventes=ventes)
        self.assertIsInstance(avg_price_per_street, Dict)
        self.assertEqual(
            avg_price_per_street,
            {
                "TSSE ALLEES DU BOIS": 833.33,
                "RUE DE LA PREFECTURE": 884.15,
                "AV DE LOUISVILLE": 936.5,
                "RUE DE LEYDE": 980.39,
                "ALL DE LA MOSSON": 1030.3,
            },
        )
        self.assertEqual(len(avg_price_per_street), 5)

    def test_get_last_sales(self):
        ventes = get_simple_sales(
            code_commune=COMMUNE["code_commune"], types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO
        )
        last_sales = get_last_sales(limit=5, ventes=ventes)
        self.assertIsInstance(last_sales, List)
        self.assertEqual(len(last_sales), 5)

    def test_get_city_data(self):
        city_data = get_city_data(code_commune=COMMUNE["code_commune"])
        self.assertIsInstance(city_data, CityData)
        self.assertEqual(
            city_data.median_m2_prices_years,
            [MedianM2Price(year=2020, value=3187.27), MedianM2Price(year=2021, value=3185.56)],
        )
        self.assertEqual(city_data.median_m2_price_maison, MedianM2Price(year=2021, value=3535))
        self.assertEqual(
            city_data.median_m2_price_maison_rooms, MedianM2PriceRoom(one=None, two=3699, three=3857, four=3535)
        )
        self.assertEqual(city_data.median_m2_price_appartement, MedianM2Price(year=2021, value=3150))
        self.assertEqual(
            city_data.median_m2_price_appartement_rooms, MedianM2PriceRoom(one=3631, two=3223, three=3041, four=2704)
        )
        self.assertIsInstance(city_data.median_m2_prices_years, List)
        self.assertIsInstance(city_data.median_m2_price_maison, MedianM2Price)
        self.assertIsInstance(city_data.median_m2_price_maison_rooms, MedianM2PriceRoom)
        self.assertIsInstance(city_data.median_m2_price_appartement, MedianM2Price)
        self.assertIsInstance(city_data.median_m2_price_appartement_rooms, MedianM2PriceRoom)
        self.assertEqual(city_data.number_of_sales, 1797)
        self.assertEqual(len(city_data.most_expensive_streets), 5)
        self.assertEqual(len(city_data.less_expensive_streets), 5)
        self.assertIsInstance(city_data.most_expensive_streets, List)
        self.assertIsInstance(city_data.less_expensive_streets, List)
        self.assertIsInstance(city_data.neighbourhoods, List)
        self.assertIsInstance(city_data.agent, Agent)
        self.assertIsInstance(city_data.price_evolution_text, str)
        self.assertEqual(
            city_data.price_evolution_text,
            "Entre 2020 et 2021, les prix de l'immobilier ont augmenté de 0%, atteignant 3185 € en 2021.",
        )

    def test_get_neighbourhoods_data(self):
        ventes = get_simple_sales(
            code_commune=COMMUNE["code_commune"], types=("Maison", "Appartement"), date_from=FIVE_YEARS_AGO
        )

        neighbourhoods_data = get_neighbourhoods_data(code_commune=COMMUNE["code_commune"], mutations=ventes)
        self.assertIsInstance(neighbourhoods_data, List)
        self.assertEqual(len(neighbourhoods_data), 1)
