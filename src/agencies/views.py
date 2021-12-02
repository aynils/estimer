communeslist = ["38260", "38270", "38800"]

from population.models import PopulationStat


def find_inhabitant_by_code_communes():
    population_stat_by_code_commune = []
    for code_commune in communeslist:
        request_by_commune = PopulationStat.objects.filter(code_commune=code_commune)
        if request_by_commune:
            population_stat_by_code_commune.append(PopulationStat.objects.filter(code_commune=code_commune))

    return population_stat_by_code_commune
