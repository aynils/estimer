from django.shortcuts import render
from population.models import PopulationStat
from agencies.models import Pricing

communeslist = ["38260", "38270"]


def find_inhabitant_by_code_communes(communeslist):
    population_stat_by_code_commune = PopulationStat.objects.filter(code_commune__in=communeslist).values_list(
        "total_population", flat=True
    )
    return population_stat_by_code_commune


def find_range_pricing():
    population = find_inhabitant_by_code_communes(communeslist)
    pricing_list = (
        Pricing.objects.filter(min_population__lt=population[1])
        .filter(max_population__gt=population[1])
        .values_list("pricing", flat=True)
    )
    return pricing_list


def communes(request):
    if request.method == "GET":
        communes = find_range_pricing()
        print(communes)
    context = {
        "communes": communes,
    }
    return render(request, "agencies/communes.html", context)
