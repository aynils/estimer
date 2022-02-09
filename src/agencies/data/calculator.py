from typing import List

from src.agencies.models import Pricing
from src.dvf.models import Commune
from src.population.models import PopulationStat


def get_cities_not_owned_by_agencies() -> List[Commune]:
    cities = Commune.objects.all().filter(agency_id__isnull=True).values("code_postal", "nom_commune", "code_commune")
    return cities


def add_population_to_cities():
    cities = get_cities_not_owned_by_agencies()
    population = PopulationStat.objects.all().values("code_commune", "total_population")
    population = {populate.get("code_commune"): populate for populate in population}
    cities_with_population = []
    for city in cities:
        code_commune = city.get("code_commune")
        total_population = population.get(code_commune, {}).get("total_population")
        city_with_population = {
            "code_commune": code_commune,
            "nom_commune": city.get("nom_commune"),
            "total_population": total_population,
        }
        cities_with_population.append(city_with_population)

    return cities_with_population


def add_pricing_to_cities():
    global total_population
    cities = add_population_to_cities()
    pricing = Pricing.objects.all().values("min_population", "max_population", "pricing")
    cities_with_pricing = []
    for city in cities:
        code_commune = city.get("code_commune")
        total_population = city.get("total_population")
        if total_population is not None:
            total_population = int(city.get("total_population"))
        else:
            total_population = 0
        for price in pricing:
            population_min = price.get("min_population")
            population_max = price.get("max_population")
            if total_population != 0:
                if total_population in range(population_min, population_max):
                    city_with_pricing = {
                        "code_commune": code_commune,
                        "nom_commune": city.get("nom_commune"),
                        "pricing": price.get("pricing"),
                    }
                    cities_with_pricing.append(city_with_pricing)

    return cities_with_pricing


def get_cities_with_pricing():
    cities_pricing = add_pricing_to_cities()
    return cities_pricing
