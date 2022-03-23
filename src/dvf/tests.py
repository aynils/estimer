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
    calculate_bar_heights,
    generate_price_evolution_text,
    get_iris_code_for_coordinates,
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
        self.assertEqual(avg_price[2021], 3142.86)
        self.assertEqual(avg_price, {ONE_YEAR_AGO.year: 3142.86})
        self.assertEqual(len(avg_price), 1)

    def test_get_avg_m2_price_rooms(self):
        ventes = get_simple_sales(
            code_commune=COMMUNE["code_commune"], types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO
        )
        avg_price_per_room = get_avg_m2_price_rooms(
            types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO, ventes=ventes
        )
        self.assertIsInstance(avg_price_per_room, Dict)
        self.assertEqual(avg_price_per_room, {1: 3600, 2: 3198, 3: 3009, 4: 2794, 5: 3043, 6: 2702, 7: 2451, 8: 1193})
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
                "RTE DE LODEVE": 2044.45,
                "RUE CHARLES BORROMEE": 1888.09,
                "RUE DES CHASSEURS": 2218.51,
                "RUE FABRI DE PEIRESC": 1500.16,
                "RUE GUILLAUME JANVIER": 2244.95,
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
            [MedianM2Price(year=2020, value=3133.7), MedianM2Price(year=2021, value=3141.2)],
        )
        self.assertEqual(city_data.median_m2_price_maison, MedianM2Price(year=2021, value=3445))
        self.assertEqual(
            city_data.median_m2_price_maison_rooms, MedianM2PriceRoom(one=None, two=3636, three=3616, four=3413)
        )
        self.assertEqual(city_data.median_m2_price_appartement, MedianM2Price(year=2021, value=3120))
        self.assertEqual(
            city_data.median_m2_price_appartement_rooms, MedianM2PriceRoom(one=3617, two=3171, three=3006, four=2505)
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
            "Entre 2020 et 2021, les prix de l'immobilier ont augmenté de 0%, atteignant 3141 € en 2021.",
        )

    def test_get_neighbourhoods_data(self):
        ventes = get_simple_sales(
            code_commune=COMMUNE["code_commune"], types=("Maison", "Appartement"), date_from=FIVE_YEARS_AGO
        )

        neighbourhoods_data = get_neighbourhoods_data(code_commune=COMMUNE["code_commune"], mutations=ventes)
        self.assertIsInstance(neighbourhoods_data, List)
        self.assertEqual(len(neighbourhoods_data), 1)

    def test_calculate_bar_heights(self):
        ventes = get_simple_sales(
            code_commune=COMMUNE["code_commune"], types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO
        )
        avg_price = get_avg_m2_price_per_year(types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO, ventes=ventes)
        bar_heights = calculate_bar_heights(avg_price)
        self.assertIsInstance(bar_heights, Dict)
        self.assertEqual(bar_heights, {"2021": {"height": 145, "text_y": 25, "value": 3142, "y": 35}})

    def test_generate_price_evolution_text(self):
        ventes = get_simple_sales(
            code_commune=COMMUNE["code_commune"], types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO
        )
        avg_price = get_avg_m2_price_per_year(types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO, ventes=ventes)
        price_evolution_text = generate_price_evolution_text(avg_price)
        self.assertIsInstance(price_evolution_text, str)
        self.assertEqual(
            price_evolution_text,
            "Entre 2020 et 2021, les prix de l'immobilier ont augmenté de 0%, atteignant 3142 € en 2021.",
        )

    def test_get_iris_code_for_coordinates(self):
        sales = get_simple_sales(
            code_commune=COMMUNE["code_commune"], types=("Maison", "Appartement"), date_from=ONE_YEAR_AGO
        )
        iris_code = get_iris_code_for_coordinates(
            latitude=float(sales.latitude[0]), longitude=float(sales.longitude[0])
        )
        self.assertIsInstance(iris_code, str)
        self.assertEqual(iris_code, "341721201")

    def test_median_m2_prices_appartement(self):
        ventes = get_simple_sales(
            code_commune=COMMUNE["code_commune"], types=("Maison", "Appartement"), date_from=FIVE_YEARS_AGO
        )

        median_m2_prices_appartement = get_avg_m2_price_per_year(
            types=("Appartement",), date_from=ONE_YEAR_AGO, ventes=ventes
        )
        self.assertIsInstance(median_m2_prices_appartement, Dict)
        self.assertEqual(median_m2_prices_appartement, {2021: 3120.0})

    def test_median_m2_prices_maison(self):
        ventes = get_simple_sales(
            code_commune=COMMUNE["code_commune"], types=("Maison", "Appartement"), date_from=FIVE_YEARS_AGO
        )
        median_m2_prices_maison = get_avg_m2_price_per_year(types=("Maison",), date_from=ONE_YEAR_AGO, ventes=ventes)
        self.assertIsInstance(median_m2_prices_maison, Dict)
        self.assertEqual(median_m2_prices_maison, {2021: 3445.36})
