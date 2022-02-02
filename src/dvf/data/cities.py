import base64
import datetime
from typing import List, Tuple
import json

import math
import pandas as pd
from django.contrib.gis.geos import Point
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.conf import settings

from src.agencies.models import Agency
from src.dvf.data.classes import (
    Address,
    Agent,
    CityData,
    ClosebyCity,
    Geometry,
    MapMarker,
    MedianM2Price,
    MedianM2PriceRoom,
    Sale,
    StreetMedianPrice,
    NeighbourhoodPolygon,
    Neighbourhood,
    PolygonColor,
)
from src.dvf.models import Commune, ValeursFoncieres
from src.helpers.cache import cached_function
from src.iris.models import IRIS

# from helpers.timer import timer

TODAY = datetime.date.today()
ONE_YEAR_AGO = datetime.date(year=TODAY.year - 1, month=1, day=1)
FIVE_YEARS_AGO = datetime.date(year=TODAY.year - 5, month=1, day=1)


# @timer
def get_avg_m2_price_per_year(types: Tuple, date_from: datetime.date, ventes: pd.DataFrame) -> dict:
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
def get_avg_m2_price_street(limit: int, ascending: bool, ventes: pd.DataFrame) -> dict:
    if ventes.empty:
        return {}

    average_per_street = ventes.groupby("adresse_nom_voie").mean().round(2)
    return average_per_street.sort_values(by="prix_m2", ascending=ascending).head(n=limit)["prix_m2"].to_dict()


# @timer
def get_last_sales(limit: int, ventes: pd.DataFrame) -> dict:
    ordered_sales = ventes.sort_values(by="date_mutation", ascending=False)
    return ordered_sales.head(n=limit).to_dict("records")


def remove_outliers(data_frame: pd.DataFrame, column_name: str) -> pd.DataFrame:
    q1 = data_frame[column_name].quantile(0.01)
    q3 = data_frame[column_name].quantile(0.99)

    return data_frame.loc[(data_frame[column_name].between(q1, q3))]


# @timer
@cached_function(ttl=settings.CACHE_TTL_ONE_DAY)
def get_city_data(code_commune: str) -> CityData:
    ventes = get_simple_sales(code_commune=code_commune, types=("Maison", "Appartement"), date_from=FIVE_YEARS_AGO)

    median_m2_prices_appartement = get_avg_m2_price_per_year(
        types=("Appartement",), date_from=ONE_YEAR_AGO, ventes=ventes
    )
    if median_m2_prices_appartement.get(ONE_YEAR_AGO.year):
        median_m2_price_appartement = MedianM2Price(
            value=int(median_m2_prices_appartement[ONE_YEAR_AGO.year]), year=ONE_YEAR_AGO.year
        )
    else:
        median_m2_price_appartement = None

    median_m2_prices_maison = get_avg_m2_price_per_year(types=("Maison",), date_from=ONE_YEAR_AGO, ventes=ventes)

    median_m2_prices_room_maison = get_avg_m2_price_rooms(types=("Maison",), date_from=FIVE_YEARS_AGO, ventes=ventes)

    median_m2_prices_rooms_maison = MedianM2PriceRoom(
        one=median_m2_prices_room_maison.get(1),
        two=median_m2_prices_room_maison.get(2),
        three=median_m2_prices_room_maison.get(3),
        four=median_m2_prices_room_maison.get(4),
    )

    median_m2_prices_room_appartement = get_avg_m2_price_rooms(
        types=("Appartement",), date_from=FIVE_YEARS_AGO, ventes=ventes
    )

    median_m2_prices_rooms_appartement = MedianM2PriceRoom(
        one=median_m2_prices_room_appartement.get(1),
        two=median_m2_prices_room_appartement.get(2),
        three=median_m2_prices_room_appartement.get(3),
        four=median_m2_prices_room_appartement.get(4),
    )

    if median_m2_prices_maison.get(ONE_YEAR_AGO.year):
        median_m2_price_maison = MedianM2Price(
            value=int(median_m2_prices_maison[ONE_YEAR_AGO.year]), year=ONE_YEAR_AGO.year
        )
    else:
        median_m2_price_maison = None

    avg_m2_price = get_avg_m2_price_per_year(
        types=("Maison", "Appartement"), date_from=FIVE_YEARS_AGO, ventes=ventes
    ).items()

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

    # map_markers = generate_map_markers(last_sales=last_sales)

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

    chart_b64_svg = generate_chart_b64_svg(bar_heights=bar_heights, city_name=city_name)

    neighbourhoods = get_neighbourhoods_data(
        code_commune=code_commune, date_from=FIVE_YEARS_AGO, types=("Maison", "Appartement")
    )

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
        # map_markers=map_markers,
        neighbourhoods=neighbourhoods,
    )


def get_neighbourhoods_data(code_commune: str, date_from: datetime.date, types: tuple) -> List[NeighbourhoodPolygon]:
    iris_list = IRIS.objects.values("geometry", "code_iris").filter(insee_commune=code_commune).all()
    neighbourhoods = []
    mutations = get_avg_m2_price_per_iris(code_commune=code_commune, date_from=date_from, types=types)
    for iris in iris_list:
        code_iris = iris.get("code_iris")
        average_m2_price = mutations.get(code_iris)
        if average_m2_price:
            neighbourhood = Neighbourhood(
                average_m2_price=f"{int(average_m2_price)} €",
                code_iris=code_iris,
                color=define_polygon_color(m2_price=average_m2_price),
            )
            geometry = iris.get("geometry")
            geojson = json.loads(geometry.geojson)
            geojson["coordinates"] = convert_coordinates_srid(
                initial_srid=geometry.srid, new_srid=4326, coordinates=geojson.get("coordinates")
            )
            neighbourhoods.append(NeighbourhoodPolygon(geometry=geojson, properties=neighbourhood))

    return neighbourhoods


# @timer
@cached_function(ttl=settings.CACHE_TTL_SIX_MONTH)
def get_simple_sales(code_commune: str, types: Tuple, date_from: datetime.date) -> pd.DataFrame:
    columns = [
        "valeur_fonciere",
        "surface_reelle_bati",
        "date_mutation",
        "adresse_nom_voie",
        "type_local",
        "adresse_numero",
        "adresse_suffixe",
        "nombre_pieces_principales",
        "longitude",
        "latitude",
        "id_mutation",
    ]

    queryset = (
        ValeursFoncieres.objects.filter(code_commune=code_commune)
        .filter(type_local__in=types)
        .filter(date_mutation__gt=date_from)
        .filter(longitude__isnull=False)
        .filter(latitude__isnull=False)
        .values_list(*columns)
    )

    mutations = pd.DataFrame.from_records(queryset, columns=columns)

    return cleanup_mutations(mutations=mutations)


# @timer
def cleanup_mutations(mutations: pd.DataFrame) -> pd.DataFrame:
    unique_mutations = mutations.drop_duplicates(subset="id_mutation", keep=False)
    unique_mutations["prix_m2"] = (
        unique_mutations["valeur_fonciere"] / unique_mutations["surface_reelle_bati"]
    ).astype("float")
    unique_mutations["annee"] = pd.DatetimeIndex(unique_mutations["date_mutation"]).year
    unique_mutations = unique_mutations.round({"prix_m2": 2})

    return remove_outliers(unique_mutations, "prix_m2")


@cached_function(ttl=settings.CACHE_TTL_SIX_MONTH)
def get_cities() -> List[Commune]:
    return Commune.objects.all()


@cached_function(ttl=settings.CACHE_TTL_SIX_MONTH)
def get_city_from_slug(slug: str) -> Commune or None:
    try:
        return Commune.objects.get(slug=slug)
    except Commune.DoesNotExist:
        return None


# @timer
@cached_function(ttl=settings.CACHE_TTL_SIX_MONTH)
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
        max_year = 2022
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
        MapMarker(geometry=Geometry(coordinates=[sale.address.longitude, sale.address.latitude]), properties=sale)
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
            y="{bar_heights.get('2017', {}).get('text_y')}">
                {bar_heights.get('2017', {}).get('value')} €
            </text>
            <rect x="30" y="{bar_heights.get('2017', {}).get('y')}" width="60"
                  height="{bar_heights.get('2017', {}).get('height')}"
                  style="fill:#1378f8"></rect>
            <text font-family="Rubik, sans-serif" class="svg-text" x="40" y="200">
                2017
            </text>
            <text font-family="Rubik, sans-serif"
            class="svg-text" x="155" y="{bar_heights.get('2018', {}).get('text_y')}">
                {bar_heights.get('2018', {}).get('value')} €
            </text>
            <rect x="150" y="{bar_heights.get('2018', {}).get('y')}" width="60"
                  height="{bar_heights.get('2018', {}).get('height')}"
                  style="fill:#1378f8"></rect>
            <text font-family="Rubik, sans-serif" class="svg-text" x="160" y="200">
                2018
            </text>
            <text font-family="Rubik, sans-serif"
            class="svg-text" x="275" y="{bar_heights.get('2019', {}).get('text_y')}">
                {bar_heights.get('2019', {}).get('value')} €
            </text>
            <rect x="270" y="{bar_heights.get('2019', {}).get('y')}" width="60"
                  height="{bar_heights.get('2019', {}).get('height')}"
                  style="fill:#1378f8"></rect>
            <text font-family="Rubik, sans-serif" class="svg-text" x="280" y="200">
                2019
            </text>
            <text font-family="Rubik, sans-serif"
            class="svg-text" x="395" y="{bar_heights.get('2020', {}).get('text_y')}">
                {bar_heights.get('2020', {}).get('value')} €
            </text>
            <rect x="390" y="{bar_heights.get('2020', {}).get('y')}" width="60"
                  height="{bar_heights.get('2020', {}).get('height')}"
                  style="fill:#1378f8"></rect>
            <text font-family="Rubik, sans-serif" class="svg-text" x="400" y="200">
                2020
            </text>
            <text font-family="Rubik, sans-serif"
            class="svg-text" x="515" y="{bar_heights.get('2021', {}).get('text_y')}">
                {bar_heights.get('2021', {}).get('value')} €
            </text>
            <rect x="510" y="{bar_heights.get('2021', {}).get('y')}" width="60"
                  height="{bar_heights.get('2021', {}).get('height')}"
                  style="fill:#1378f8"></rect>
            <text font-family="Rubik, sans-serif" class="svg-text" x="520" y="200">
                2021
            </text>
        </svg>"""

    encoded_svg = svg.encode("utf-8")
    b64_svg = base64.b64encode(encoded_svg)

    return b64_svg.decode("utf-8")


def get_closeby_cities(code_postal: str) -> List[ClosebyCity]:
    cities_under = Commune.objects.filter(code_postal__lt=code_postal).order_by("-code_postal")[:15].all()
    cities_over = Commune.objects.filter(code_postal__gt=code_postal).order_by("code_postal")[:15].all()
    return [
        ClosebyCity(nom_commune=city.nom_commune, slug=city.slug) for city in list(cities_under) + list(cities_over)
    ]


def get_iris_code_for_coordinates(longitude: float, latitude: float):
    point = Point(longitude, latitude, srid=4326)
    point.transform(2154)

    iris = IRIS.objects.filter(geometry__contains=point).first()

    return iris.code_iris


def get_mutations_for_iris(code_iris: str, date_from: datetime.date) -> pd.DataFrame:
    iris = IRIS.objects.get(code_iris=code_iris)
    code_commune = iris.insee_commune

    mutations = get_simple_sales(code_commune=code_commune, types=("Maison", "Appartement"), date_from=date_from)
    mutations = add_iris_to_mutations(mutations=mutations)
    filtered_mutations = mutations[mutations["code_iris"] == code_iris]

    return filtered_mutations


def add_iris_to_mutations(mutations: pd.DataFrame) -> pd.DataFrame:
    mutations["code_iris"] = mutations.apply(
        lambda row: get_iris_code_for_coordinates(float(row["longitude"]), float(row["latitude"])), axis=1
    )
    return mutations


def get_avg_m2_price_per_iris(code_commune: str, date_from: datetime.date, types: tuple) -> pd.DataFrame:
    mutations = get_simple_sales(code_commune=code_commune, types=types, date_from=date_from)
    mutations = add_iris_to_mutations(mutations=mutations)
    return mutations.groupby("code_iris").mean().round(2)["prix_m2"].to_dict()


def convert_coordinates_srid(
    initial_srid: int, new_srid: int, coordinates: List[List[List[List[float]]]]
) -> List[List[List[List[float]]]]:
    initial_srid = SpatialReference(initial_srid)
    new_srid = SpatialReference(new_srid)
    transform_method = CoordTransform(initial_srid, new_srid)
    converted_coordinates = []
    for coordinate in coordinates:
        converted_sub = []
        for sub in coordinate:
            converted_points = []
            for sub_sub in sub:
                point = Point(*sub_sub, srid=initial_srid)
                point.transform(transform_method)
                converted_points.append(list(point.ogr.coords))
            converted_sub.append(converted_points)
        converted_coordinates.append(converted_sub)

    return converted_coordinates


def define_polygon_color(m2_price: float) -> PolygonColor:
    if m2_price >= 4500:
        return PolygonColor(background="#0B3C93", text="#F2F7FF")
    elif m2_price >= 4000:
        return PolygonColor(background="#105ADC", text="#F2F7FF")
    elif m2_price >= 3500:
        return PolygonColor(background="#3F80F1", text="#F2F7FF")
    elif m2_price >= 3000:
        return PolygonColor(background="#7FAAF6", text="#F2F7FF")
    elif m2_price >= 2500:
        return PolygonColor(background="#BAD1F8", text="#15171A")
    elif m2_price >= 2000:
        return PolygonColor(background="#BFD5FA", text="#15171A")
    elif m2_price >= 1500:
        return PolygonColor(background="#DFEAFD", text="#15171A")
    else:
        return PolygonColor(background="#F2F7FF", text="#15171A")
