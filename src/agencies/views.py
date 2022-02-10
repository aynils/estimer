from django.shortcuts import render

from src.agencies.data.calculator import get_cities_with_pricing


def agency(request):
    code_departement = request.GET.get("code_departement")
    if code_departement:
        cities_pricing = get_cities_with_pricing(code_departement)
    else:
        cities_pricing = []
    context = {
        "cities_pricing": [
            {
                "id": pricing.get("id"),
                "zipcode": pricing.get("code_postal"),
                "name": pricing.get("nom_commune"),
                "price": pricing.get("pricing"),
            }
            for pricing in cities_pricing
        ]
    }
    return render(request, "agencies/agency.html", context)
