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
    communes = find_inhabitant_by_code_communes(communeslist)
    range_pricing = Pricing.objects.all()
    communes_list = []
    for range in range_pricing:
        min_population = range.min_population
        max_population = range.max_population
        for commune in communes:
            if min_population <= commune <= max_population:
                communes_list.append(commune)
                communes_list.append(range)
    return communes_list


def communes(request):
    if request.method == "GET":
        communes = find_range_pricing()
        print(communes)
    context = {
        "communes": communes,
    }
    return render(request, "agencies/communes.html", context)
