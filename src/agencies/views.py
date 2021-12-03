import pandas as pd
from django.shortcuts import render
from population.models import PopulationStat
from agencies.models import Tench

communeslist = ["38260", "38270"]


def find_inhabitant_by_code_communes():
    population_stat_by_code_commune = PopulationStat.objects.filter(code_commune__in=communeslist)
    return population_stat_by_code_commune


def find_range_pricing():
    communes = find_inhabitant_by_code_communes()
    range_pricing = Tench.objects.all()
    communes_list = []
    for range in range_pricing:
        min_habitant = range.min_inhabitant
        max_habitant = range.max_inhabitant
        for commune in communes:
            if min_habitant <= commune.total_population <= max_habitant:
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
