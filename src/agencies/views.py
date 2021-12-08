from typing import List

from django.shortcuts import render
from population.models import PopulationStat
from agencies.models import Pricing

communes_list = ["38260", "38270"]


def find_population_by_code_communes(communes_list: List[str]) -> List[float]:
    population_stat_by_code_commune = PopulationStat.objects.filter(code_commune__in=communes_list).values_list(
        "total_population", flat=True
    )
    return population_stat_by_code_commune


def calculate_pricing():
    population_list = find_population_by_code_communes(communes_list)
    pricing_list = []
    for population in population_list:
        pricing = (
            Pricing.objects.filter(min_population__lte=population)
            .filter(max_population__gte=population)
            .only("pricing")
            .first()
        )
        if pricing:
            pricing_list.append(pricing.pricing)
    return sum(pricing_list)


def get_pricing(request):
    if request.method == "GET":
        pricing = calculate_pricing()
    context = {
        "pricing": pricing,
    }
    return render(request, "agencies/communes.html", context)
