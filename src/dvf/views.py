from django.shortcuts import render
import requests

from dvf.data.cities import get_city_data, get_city_from_slug, get_city_from_code

SEARCH_API_URL = 'https://api-adresse.data.gouv.fr/search/'


def city(request, slug):
    if request.method == "GET":
        commune = get_city_from_slug(slug=slug)
        if commune:
            city_data = get_city_data(code_commune=commune.code_commune)
            context = {
                "slug": slug,
                "city_name": commune.nom_commune,
                "city_data": city_data,
                "title": f'Prix m2 {commune.nom_commune} ({commune.code_departement}) '
                         f'| Prix immobilier et estimation à {commune.nom_commune}'
            }

            return render(request, "dvf/city.html", context)

        else:
            context = {
                "city_slug": slug
            }
            return render(request, "dvf/404.html", context)

    elif request.method == "POST":
        address = request.POST.get('address')
        params = {
            "q" : address
        }
        headers = {
            "Accept": "application/json"
        }
        response = requests.get(url=SEARCH_API_URL, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            properties = data.get('features',[])[0].get('properties',{})
            city_code = properties.get('citycode')

            commune = get_city_from_code(code=city_code)
            if commune:
                city_data = get_city_data(code_commune=commune.code_commune)
                context = {
                    "slug": commune.slug,
                    "city_name": commune.nom_commune,
                    "city_data": city_data,
                    "title": f'Prix m2 {commune.nom_commune} ({commune.code_departement}) '
                             f'| Prix immobilier et estimation à {commune.nom_commune}'
                }

                return render(request, "dvf/city.html", context)

            else:
                context = {
                    "city_slug": slug
                }
                return render(request, "dvf/404.html", context)
