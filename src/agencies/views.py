from django.shortcuts import render
from population.models import PopulationStat

communeslist = ["38260", "38270"]


def find_inhabitant_by_code_communes():
    population_stat_by_code_commune = PopulationStat.objects.filter(code_commune__in=communeslist).values()
    return population_stat_by_code_commune.values


def communes(request):
    if request.method == "GET":
        communes = find_inhabitant_by_code_communes()
    context = {
        "communes": communes,
    }
    return render(request, "agencies/communes.html", context)
