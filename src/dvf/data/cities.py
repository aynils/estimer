from typing import Tuple, List
import datetime
import pandas as pd
from django.db import connection
# from helpers.timer import timer
# @timer
from dvf.models import ValeursFoncieres
from dvf.data.classes import CityData, MedianM2Price, Sale, Address, StreetMedianPrice


def get_avg_m2_price(code_commune: int,
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
def get_avg_m2_price_street(code_commune: int,
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


def get_last_sales(code_commune: int,
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


def get_count_sales(code_commune: int,
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
def get_city_data(code_commune: int) -> CityData:
    today = datetime.date.today()
    last_year = datetime.date(year=today.year - 1, month=1, day=1)
    last_5_years = datetime.date(year=today.year - 5, month=1, day=1)

    median_m2_prices_appartement = get_avg_m2_price(code_commune=code_commune,
                                                    types=('Appartement',),
                                                    date_from=last_year)
    if median_m2_prices_appartement.get(last_year.year):
        median_m2_price_appartement = MedianM2Price(
            value=median_m2_prices_appartement[last_year.year],
            year=last_year.year)
    else:
        median_m2_price_appartement = None

    median_m2_prices_maison = get_avg_m2_price(code_commune=code_commune,
                                               types=('Maison',),
                                               date_from=last_year)

    if median_m2_prices_maison.get(last_year.year):
        median_m2_price_maison = MedianM2Price(
            value=median_m2_prices_maison[last_year.year],
            year=last_year.year)
    else:
        median_m2_price_maison = None

    median_m2_prices_years = [MedianM2Price(
        value=price,
        year=year) for year, price in get_avg_m2_price(code_commune=code_commune,
                                                       types=('Maison', 'Appartement'),
                                                       date_from=last_5_years).items()]

    last_sales = [Sale(
        date=sale.get('date_mutation'),
        price=sale.get('valeur_fonciere'),
        surface=sale.get('surface_reelle_bati'),
        m2_price=sale.get('prix_m2'),
        type_local=sale.get('type_local'),
        rooms_count=sale.get('nombre_pieces_principales'),
        address=Address(
            numero=sale.get('adresse_numero'),
            suffixe=sale.get('adresse_suffixe'),
            nom_voie=sale.get('adresse_nom_voie'),
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
        nom_voie=rue,
        avg_m2_price=price
    ) for rue, price in get_avg_m2_price_street(limit=5,
                                                code_commune=code_commune,
                                                types=('Maison', 'Appartement'),
                                                ascending=False,
                                                date_from=last_5_years
                                                ).items()]

    less_expensive_streets = [StreetMedianPrice(
        nom_voie=rue,
        avg_m2_price=price
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

    return CityData(
        code_commune=code_commune,
        median_m2_price_appartement=median_m2_price_appartement,
        median_m2_price_maison=median_m2_price_maison,
        median_m2_prices_years=median_m2_prices_years,
        last_sales=last_sales,
        most_expensive_streets=most_expensive_streets,
        less_expensive_streets=less_expensive_streets,
        number_of_sales=number_of_sales or 0,
    )


def get_all_cities(limit: int = None) -> list:
    return get_cities(limit=limit,
                      types=['Maison'],
                      years=[2016, 2017, 2018, 2019, 2020])


# noinspection SqlResolve
def get_simple_sales(code_commune: int,
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


def get_cities(types: List[str],
               years: List[int],
               limit: int = None) -> List[dict]:
    results = (
        ValeursFoncieres.objects
            .filter(type_local__in=types)
            .filter(date_mutation__year__in=years)[:limit]
    ).distinct('code_commune')

    return [{"name": result.nom_commune,
             "code": result.code_commune,
             "code_departement": result.code_departement,
             "code_postal": result.code_postal,
             } for result in results]
