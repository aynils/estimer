import datetime
from typing import Tuple, List
from helpers.cache import cached_function
from estimer.settings import CACHE_TTL_SIX_MONTH, CACHE_TTL_ONE_DAY
from django.core.exceptions import ObjectDoesNotExist

import pandas as pd
from django.db import connection

from dvf.data.classes import CityData, MedianM2Price, Sale, Address, StreetMedianPrice, Agent
# from helpers.timer import timer

from dvf.models import Commune

# @timer
def get_avg_m2_price(code_commune: str,
                     types: Tuple,
                     date_from: datetime.date) -> dict:
    ventes = get_simple_sales(code_commune=code_commune,
                              types=types,
                              date_from=date_from)

    if ventes.empty:
        return {}

    clean_vente_per_year = remove_outliers(ventes, 'prix_m2')
    return clean_vente_per_year.groupby('annee').mean().round(2)['prix_m2'].to_dict()


# @timer
def get_avg_m2_price_street(code_commune: str,
                            types: Tuple,
                            limit: int,
                            ascending: bool,
                            date_from: datetime.date) -> dict:
    ventes = get_simple_sales(code_commune=code_commune,
                              types=types,
                              date_from=date_from)

    if ventes.empty:
        return {}

    average_per_street = ventes.groupby('adresse_nom_voie').mean().round(2)
    clean_average_per_street = remove_outliers(average_per_street, 'prix_m2')
    return (clean_average_per_street
            .sort_values(by="prix_m2", ascending=ascending)
            .head(n=limit)["prix_m2"]
            .to_dict())


def get_last_sales(code_commune: str,
                   types: Tuple,
                   date_from: datetime.date,
                   limit: int) -> dict:
    ventes = get_simple_sales(code_commune=code_commune,
                              types=types,
                              date_from=date_from)

    ordered_sales = ventes.sort_values(by="date_mutation", ascending=False)
    clean_sales = remove_outliers(ordered_sales, 'valeur_fonciere')
    return (clean_sales
            .head(n=limit)
            .round(2)
            .to_dict('records'))


def get_count_sales(code_commune: str,
                    types: Tuple,
                    date_from: datetime.date) -> int:
    ventes = get_simple_sales(code_commune=code_commune,
                              types=types,
                              date_from=date_from)

    return ventes.__len__()


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

    median_m2_prices_appartement = get_avg_m2_price(code_commune=code_commune,
                                                    types=('Appartement',),
                                                    date_from=last_year)
    if median_m2_prices_appartement.get(last_year.year):
        median_m2_price_appartement = MedianM2Price(
            value=int(median_m2_prices_appartement[last_year.year]),
            year=last_year.year)
    else:
        median_m2_price_appartement = None

    median_m2_prices_maison = get_avg_m2_price(code_commune=code_commune,
                                               types=('Maison',),
                                               date_from=last_year)

    if median_m2_prices_maison.get(last_year.year):
        median_m2_price_maison = MedianM2Price(
            value=int(median_m2_prices_maison[last_year.year]),
            year=last_year.year)
    else:
        median_m2_price_maison = None

    avg_m2_price = get_avg_m2_price(code_commune=code_commune,
                                    types=('Maison', 'Appartement'),
                                    date_from=last_5_years).items()

    median_m2_prices_years = [MedianM2Price(
        value=price,
        year=year) for year, price in avg_m2_price]

    bar_heights = calculate_bar_heights(avg_m2_price=dict(avg_m2_price))

    price_evolution_text = generate_price_evolution_text(dict(avg_m2_price))

    last_sales = [Sale(
        date=sale.get('date_mutation').date,
        price=int(sale.get('valeur_fonciere')) if sale.get('valeur_fonciere') else '',
        surface=int(sale.get('surface_reelle_bati')) if sale.get('surface_reelle_bati') else '',
        m2_price=int(sale.get('prix_m2')) if sale.get('prix_m2') else '',
        type_local=sale.get('type_local'),
        rooms_count=sale.get('nombre_pieces_principales'),
        address=Address(
            numero=int(sale.get('adresse_numero')) if sale.get('adresse_numero') else '',
            suffixe=sale.get('adresse_suffixe'),
            nom_voie=sale.get('adresse_nom_voie', '').lower(),
            code_voie=sale.get('adresse_code_voie'),
            code_postal=sale.get('code_postal'),
            code_commune=sale.get('code_commune'),
            code_departement=sale.get('code_departement'),
        )
    ) for sale in get_last_sales(limit=10,
                                 code_commune=code_commune,
                                 types=('Maison', 'Appartement'),
                                 date_from=last_5_years)]

    most_expensive_streets = [StreetMedianPrice(
        nom_voie=rue.lower(),
        avg_m2_price=int(price)
    ) for rue, price in get_avg_m2_price_street(limit=5,
                                                code_commune=code_commune,
                                                types=('Maison', 'Appartement'),
                                                ascending=False,
                                                date_from=last_5_years
                                                ).items()]

    less_expensive_streets = [StreetMedianPrice(
        nom_voie=rue.lower(),
        avg_m2_price=int(price)
    ) for rue, price in get_avg_m2_price_street(limit=5,
                                                code_commune=code_commune,
                                                types=('Maison', 'Appartement'),
                                                ascending=True,
                                                date_from=last_5_years
                                                ).items()]

    number_of_sales = get_count_sales(
        code_commune=code_commune,
        types=('Maison', 'Appartement'),
        date_from=last_5_years
    )

    agent = get_agent(code_commune=code_commune)

    return CityData(
        code_commune=code_commune,
        median_m2_price_appartement=median_m2_price_appartement,
        median_m2_price_maison=median_m2_price_maison,
        median_m2_prices_years=median_m2_prices_years,
        last_sales=last_sales,
        most_expensive_streets=most_expensive_streets,
        less_expensive_streets=less_expensive_streets,
        number_of_sales=number_of_sales or 0,
        agent=agent,
        bar_heights=bar_heights,
        price_evolution_text=price_evolution_text
    )


def get_all_cities() -> list:
    return get_cities()


# noinspection SqlResolve
@cached_function(ttl=CACHE_TTL_SIX_MONTH)
def get_simple_sales(code_commune: str,
                     types: Tuple,
                     date_from: datetime.date) -> pd.DataFrame:
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
        CAST((valeur_fonciere / surface_reelle_bati) as DECIMAL(16,2)) as prix_m2,
        EXTRACT(year FROM dvf_valeursfoncieres.date_mutation) as annee
        FROM dvf_valeursfoncieres
            WHERE code_commune = %(code_commune)s
            AND type_local in %(types)s
            AND date_mutation >= %(date_from)s""",
        connection,
        params={
            "code_commune": str(code_commune),
            "date_from": date_from,
            "types": types
        },
        parse_dates=["date_mutation"]
    )

    return mutations.drop_duplicates(subset="id_mutation", keep=False)

@cached_function(ttl=CACHE_TTL_SIX_MONTH)
def get_cities() -> List[Commune]:
    return Commune.objects.all()

@cached_function(ttl=CACHE_TTL_SIX_MONTH)
def get_city_from_slug(slug: str) -> Commune:
    try:
        return Commune.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return None


def get_agent(code_commune: str) -> Agent:
    return Agent(
        picture='https://estimer-prod.fra1.cdn.digitaloceanspaces.com/static/estimer/images/olivier.jpeg',
        name='Olivier Pourquier',
        agency='estimer.com',
        description='''Vous souhaitez obtenir une estimation précise de votre bien ?
        Nous vous mettons en relation avec un agent immobilier local, expert sur votre secteur.''',
        phone_number='06.81.37.36.33',
        email='contact@estimer.com',
        website_url='estimer.com',
    )


def calculate_bar_heights(avg_m2_price: dict) -> dict:
    max_price = max(avg_m2_price.values())
    return {
        key: {
            "height": int(value / max_price * 135),
            "value": int(value),
        }
        for key, value in avg_m2_price.items()}


def generate_price_evolution_text(avg_m2_price: dict) -> str:
    max_year = int(max(avg_m2_price.keys()))
    max_year_price = int(avg_m2_price.get(max_year, 0))
    last_year_price = int(
            avg_m2_price.get(max_year - 1)
            or avg_m2_price.get(max_year - 2)
            or avg_m2_price.get(max_year - 3)
            or avg_m2_price.get(max_year - 4)
            or avg_m2_price.get(max_year - 5)
            or max_year_price
    )

    evolution = int((max_year_price/last_year_price) * 100 - 100)
    if evolution >= 0:
        evolution_text = f"augmenté de {evolution}"
    else:
        evolution_text = f"diminué de {abs(evolution)}"

    return f"Entre {max_year -1} et {max_year}, les prix de l'immobilier ont {evolution_text}%" \
           f", atteignant {max_year_price} € en {max_year}."
