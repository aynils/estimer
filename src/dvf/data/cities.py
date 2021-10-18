import base64
import datetime
import math
from typing import Tuple, List

import pandas as pd
from django.db import connection

from agencies.models import Agency
from dvf.data.classes import (
    CityData,
    MedianM2Price,
    Sale,
    Address,
    StreetMedianPrice,
    Agent,
    MapMarker,
    Geometry,
    ClosebyCity,
    MedianM2PriceRoom,
)
from dvf.models import Commune
from estimer.settings import CACHE_TTL_SIX_MONTH, CACHE_TTL_ONE_DAY
from helpers.cache import cached_function


# from helpers.timer import timer


# @timer
def get_avg_m2_price(types: Tuple, date_from: datetime.date, ventes: pd.DataFrame) -> dict:
    if ventes.empty:
        return {}

    ventes_subset = ventes[(ventes["annee"] >= date_from.year) & (ventes["type_local"].isin(types))]

    return ventes_subset.groupby("annee").mean().round(2)["prix_m2"].to_dict()


def get_avg_m2_price_rooms(types: Tuple, date_from: datetime.date, ventes: pd.DataFrame) -> dict:
    if ventes.empty:
        return {}

    ventes_subset = ventes[(ventes["annee"] >= date_from.year) & (ventes["type_local"].isin(types))]

    return ventes_subset.groupby("nombre_pieces_principales").mean().round(0)["prix_m2"].astype(int).to_dict()


# @timer
def get_avg_m2_price_street(
    limit: int,
    ascending: bool,
    ventes: pd.DataFrame,
) -> dict:
    if ventes.empty:
        return {}

    average_per_street = ventes.groupby("adresse_nom_voie").mean().round(2)
    # clean_average_per_street = remove_outliers(average_per_street, "prix_m2")
    return average_per_street.sort_values(by="prix_m2", ascending=ascending).head(n=limit)["prix_m2"].to_dict()


# @timer
def get_last_sales(
    limit: int,
    ventes: pd.DataFrame,
) -> dict:
    ordered_sales = ventes.sort_values(by="date_mutation", ascending=False)
    # clean_sales = remove_outliers(ordered_sales, "valeur_fonciere")
    return ordered_sales.head(n=limit).to_dict("records")


def remove_outliers(data_frame: pd.DataFrame, column_name: str) -> pd.DataFrame:
    q1 = data_frame[column_name].quantile(0.01)
    q3 = data_frame[column_name].quantile(0.99)

    return data_frame.loc[(data_frame[column_name].between(q1, q3))]


# @timer
@cached_function(ttl=CACHE_TTL_ONE_DAY)
def get_city_data(code_commune: str) -> CityData:
    today = datetime.date.today()
    last_year = datetime.date(year=today.year - 1, month=1, day=1)
    last_5_years = datetime.date(year=today.year - 5, month=1, day=1)

    ventes = get_simple_sales(
        code_commune=code_commune,
        types=("Maison", "Appartement"),
        date_from=last_5_years,
    )

    median_m2_prices_appartement = get_avg_m2_price(types=("Appartement",), date_from=last_year, ventes=ventes)
    if median_m2_prices_appartement.get(last_year.year):
        median_m2_price_appartement = MedianM2Price(
            value=int(median_m2_prices_appartement[last_year.year]), year=last_year.year
        )
    else:
        median_m2_price_appartement = None

    median_m2_prices_maison = get_avg_m2_price(types=("Maison",), date_from=last_year, ventes=ventes)

    median_m2_prices_room_maison = get_avg_m2_price_rooms(types=("Maison",), date_from=last_5_years, ventes=ventes)

    median_m2_prices_rooms_maison = MedianM2PriceRoom(
        one=median_m2_prices_room_maison.get(1),
        two=median_m2_prices_room_maison.get(2),
        three=median_m2_prices_room_maison.get(3),
        four=median_m2_prices_room_maison.get(4),
    )

    median_m2_prices_room_appartement = get_avg_m2_price_rooms(
        types=("Appartement",), date_from=last_5_years, ventes=ventes
    )

    median_m2_prices_rooms_appartement = MedianM2PriceRoom(
        one=median_m2_prices_room_appartement.get(1),
        two=median_m2_prices_room_appartement.get(2),
        three=median_m2_prices_room_appartement.get(3),
        four=median_m2_prices_room_appartement.get(4),
    )

    if median_m2_prices_maison.get(last_year.year):
        median_m2_price_maison = MedianM2Price(value=int(median_m2_prices_maison[last_year.year]), year=last_year.year)
    else:
        median_m2_price_maison = None

    avg_m2_price = get_avg_m2_price(types=("Maison", "Appartement"), date_from=last_5_years, ventes=ventes).items()

    median_m2_prices_years = [MedianM2Price(value=price, year=year) for year, price in avg_m2_price]

    bar_heights = calculate_bar_heights(avg_m2_price=dict(avg_m2_price))

    price_evolution_text = generate_price_evolution_text(dict(avg_m2_price))

    last_sales = [
        Sale(
            date=datetime.date(
                day=pd.to_datetime(sale.get("date_mutation")).day,
                month=pd.to_datetime(sale.get("date_mutation")).month,
                year=pd.to_datetime(sale.get("date_mutation")).year,
            ),
            price=int(sale.get("valeur_fonciere")) if sale.get("valeur_fonciere") else "",
            surface=int(sale.get("surface_reelle_bati")) if sale.get("surface_reelle_bati") else "",
            m2_price=int(sale.get("prix_m2")) if sale.get("prix_m2") else "",
            type_local=sale.get("type_local"),
            rooms_count=sale.get("nombre_pieces_principales"),
            address=Address(
                numero=int(sale.get("adresse_numero"))
                if sale.get("adresse_numero") and not math.isnan(sale.get("adresse_numero"))
                else "",
                suffixe=sale.get("adresse_suffixe"),
                nom_voie=(sale.get("adresse_nom_voie") or "").lower(),
                code_voie=sale.get("adresse_code_voie"),
                code_postal=sale.get("code_postal"),
                code_commune=sale.get("code_commune"),
                code_departement=sale.get("code_departement"),
                latitude=sale.get("latitude")
                if sale.get("latitude") and not math.isnan(sale.get("latitude"))
                else None,
                longitude=sale.get("longitude")
                if sale.get("longitude") and not math.isnan(sale.get("longitude"))
                else None,
            ),
        )
        for sale in get_last_sales(limit=20, ventes=ventes)
    ]

    map_markers = generate_map_markers(last_sales=last_sales)

    most_expensive_streets = [
        StreetMedianPrice(nom_voie=rue.lower(), avg_m2_price=int(price))
        for rue, price in get_avg_m2_price_street(limit=5, ascending=False, ventes=ventes).items()
    ]

    less_expensive_streets = [
        StreetMedianPrice(nom_voie=rue.lower(), avg_m2_price=int(price))
        for rue, price in get_avg_m2_price_street(limit=5, ascending=True, ventes=ventes).items()
    ]

    number_of_sales = ventes.__len__()

    agent = get_agent(code_commune=code_commune)

    city_name = "La cité merveilleuse"

    chart_b64_svg = generate_chart_b64_svg(city_name=city_name, bar_heights=bar_heights)

    return CityData(
        median_m2_price_appartement=median_m2_price_appartement,
        median_m2_price_appartement_rooms=median_m2_prices_rooms_appartement,
        median_m2_price_maison=median_m2_price_maison,
        median_m2_price_maison_rooms=median_m2_prices_rooms_maison,
        median_m2_prices_years=median_m2_prices_years,
        last_sales=last_sales,
        most_expensive_streets=most_expensive_streets,
        less_expensive_streets=less_expensive_streets,
        number_of_sales=number_of_sales or 0,
        agent=agent,
        chart_b64_svg=chart_b64_svg,
        price_evolution_text=price_evolution_text,
        map_markers=map_markers,
    )


def get_all_cities() -> list:
    return get_cities()


# noinspection SqlResolve
# @timer
@cached_function(ttl=CACHE_TTL_SIX_MONTH)
def get_simple_sales(code_commune: str, types: Tuple, date_from: datetime.date) -> pd.DataFrame:
    mutations = pd.read_sql(
        """SELECT
        valeur_fonciere,
        surface_reelle_bati,
        date_mutation,
        adresse_nom_voie,
        type_local,
        adresse_numero,
        adresse_suffixe,
        nombre_pieces_principales,
        id_mutation,
        code_departement,
        longitude,
        latitude,
        CAST((valeur_fonciere / surface_reelle_bati) as DECIMAL(16,2)) as prix_m2,
        EXTRACT(year FROM dvf_valeursfoncieres.date_mutation) as annee
        FROM dvf_valeursfoncieres
            WHERE code_commune = %(code_commune)s
            AND type_local in %(types)s
            AND date_mutation >= %(date_from)s
            AND longitude IS NOT NULL
            AND latitude IS NOT NULL
            """,
        connection,
        params={
            "code_commune": str(code_commune),
            "date_from": date_from,
            "types": types,
        },
        parse_dates=["date_mutation"],
    )

    unique_mutations = mutations.drop_duplicates(subset="id_mutation", keep=False)

    return remove_outliers(unique_mutations, "prix_m2")


@cached_function(ttl=CACHE_TTL_SIX_MONTH)
def get_cities() -> List[Commune]:
    return Commune.objects.all()


@cached_function(ttl=CACHE_TTL_SIX_MONTH)
def get_city_from_slug(slug: str) -> Commune or None:
    try:
        return Commune.objects.get(slug=slug)
    except Commune.DoesNotExist:
        return None


# @timer
@cached_function(ttl=CACHE_TTL_SIX_MONTH)
def get_city_from_code(code: str) -> Commune or None:
    try:
        return Commune.objects.get(code_commune=code)
    except Commune.DoesNotExist:
        return None


# @timer
def get_agent(code_commune: str) -> Agent:
    try:
        agency = Agency.objects.get(code_commune=code_commune)
        agent = Agent(
            picture=agency.picture_url,
            name=agency.agent,
            agency=agency.name,
            description=agency.description,
            phone_number=agency.phone_number,
            email=agency.email,
            website_url=agency.website_url,
        )

    except Agency.DoesNotExist:
        agent = Agent(
            picture="https://estimer.com/static/estimer/images/olivier.jpeg",
            name="Olivier Pourquier",
            agency="estimer.com",
            description="""Vous souhaitez obtenir une estimation précise de votre bien ?
                            Nous vous mettons en relation avec un agent immobilier local, expert sur votre secteur.""",
            phone_number="06.81.37.36.33",
            email="contact@estimer.com",
            website_url="estimer.com",
        )

    return agent


# @timer
def calculate_bar_heights(avg_m2_price: dict) -> dict:
    if avg_m2_price:
        max_price = max(avg_m2_price.values())
    else:
        max_price = 0
    return {
        str(int(key)): {
            "height": int(value / max_price * 145),
            "value": int(value),
            "y": 180 - int(value / max_price * 145),
            "text_y": 180 - int(value / max_price * 145) - 10,
        }
        for key, value in avg_m2_price.items()
    }


# @timer
def generate_price_evolution_text(avg_m2_price: dict) -> str:
    if avg_m2_price:
        max_year = int(max(avg_m2_price.keys()))
        max_year_price = int(avg_m2_price.get(max_year, 0))
    else:
        max_year = 2021
        max_year_price = 1

    last_year_price = int(
        avg_m2_price.get(max_year - 1)
        or avg_m2_price.get(max_year - 2)
        or avg_m2_price.get(max_year - 3)
        or avg_m2_price.get(max_year - 4)
        or avg_m2_price.get(max_year - 5)
        or max_year_price
    )

    evolution = int((max_year_price / (last_year_price or 1)) * 100 - 100)
    if evolution >= 0:
        evolution_text = f"augmenté de {evolution}"
    else:
        evolution_text = f"diminué de {abs(evolution)}"

    return (
        f"Entre {max_year - 1} et {max_year}, les prix de l'immobilier ont {evolution_text}%"
        f", atteignant {max_year_price} € en {max_year}."
    )


# @timer
def generate_map_markers(last_sales: List[Sale]) -> List[MapMarker]:
    return [
        MapMarker(
            geometry=Geometry(coordinates=[sale.address.longitude, sale.address.latitude]),
            properties=sale,
        )
        for sale in last_sales
    ]


def generate_chart_b64_svg(bar_heights: dict, city_name: str) -> str:
    svg = f"""<svg
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    viewBox="0 0 600 200"
    role="img"
    aria-labelledby="svg-title svg-desc"
        >
            <title id="svg-title">prix m2 {city_name}</title>
            <desc id="svg-desc">Evolution du prix au m2 à {city_name} pour les 5 dernières années</desc>
            <text font-family="Rubik, sans-serif"
            class="svg-text" x="35"
            y="{bar_heights.get('2016', {}).get('text_y')}">
                {bar_heights.get('2016', {}).get('value')} €
            </text>
            <rect x="30" y="{bar_heights.get('2016', {}).get('y')}" width="60"
                  height="{bar_heights.get('2016', {}).get('height')}"
                  style="fill:#1378f8"></rect>
            <text font-family="Rubik, sans-serif" class="svg-text" x="40" y="200">
                2016
            </text>
            <text font-family="Rubik, sans-serif"
            class="svg-text" x="155" y="{bar_heights.get('2017', {}).get('text_y')}">
                {bar_heights.get('2017', {}).get('value')} €
            </text>
            <rect x="150" y="{bar_heights.get('2017', {}).get('y')}" width="60"
                  height="{bar_heights.get('2017', {}).get('height')}"
                  style="fill:#1378f8"></rect>
            <text font-family="Rubik, sans-serif" class="svg-text" x="160" y="200">
                2017
            </text>
            <text font-family="Rubik, sans-serif"
            class="svg-text" x="275" y="{bar_heights.get('2018', {}).get('text_y')}">
                {bar_heights.get('2018', {}).get('value')} €
            </text>
            <rect x="270" y="{bar_heights.get('2018', {}).get('y')}" width="60"
                  height="{bar_heights.get('2018', {}).get('height')}"
                  style="fill:#1378f8"></rect>
            <text font-family="Rubik, sans-serif" class="svg-text" x="280" y="200">
                2018
            </text>
            <text font-family="Rubik, sans-serif"
            class="svg-text" x="395" y="{bar_heights.get('2019', {}).get('text_y')}">
                {bar_heights.get('2019', {}).get('value')} €
            </text>
            <rect x="390" y="{bar_heights.get('2019', {}).get('y')}" width="60"
                  height="{bar_heights.get('2019', {}).get('height')}"
                  style="fill:#1378f8"></rect>
            <text font-family="Rubik, sans-serif" class="svg-text" x="400" y="200">
                2019
            </text>
            <text font-family="Rubik, sans-serif"
            class="svg-text" x="515" y="{bar_heights.get('2020', {}).get('text_y')}">
                {bar_heights.get('2020', {}).get('value')} €
            </text>
            <rect x="510" y="{bar_heights.get('2020', {}).get('y')}" width="60"
                  height="{bar_heights.get('2020', {}).get('height')}"
                  style="fill:#1378f8"></rect>
            <text font-family="Rubik, sans-serif" class="svg-text" x="520" y="200">
                2020
            </text>
        </svg>"""

    encoded_svg = svg.encode("utf-8")
    b64_svg = base64.b64encode(encoded_svg)

    return b64_svg.decode("utf-8")


def get_closeby_cities(code_postal: str) -> List[ClosebyCity]:
    cities_under = Commune.objects.filter(code_postal__lt=code_postal).order_by("-code_postal")[:15].all()
    cities_over = Commune.objects.filter(code_postal__gt=code_postal).order_by("code_postal")[:15].all()
    return [
        ClosebyCity(
            nom_commune=city.nom_commune,
            slug=city.slug,
        )
        for city in list(cities_under) + list(cities_over)
    ]
