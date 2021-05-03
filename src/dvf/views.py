from django.shortcuts import render

from dvf.data.cities import get_city_data, get_city_from_slug


def city(request, slug):
    commune = get_city_from_slug(slug=slug)
    city_data = get_city_data(code_commune=commune.code_commune)
    context = {
        "slug": slug,
        "city_name": commune.nom_commune,
        "city_data": city_data,
        "title": f'Prix m2 {commune.nom_commune} ({commune.code_departement}) '
                 f'| Prix immobilier et estimation à {commune.nom_commune}'
    }

    return render(request, "dvf/city.html", context)
