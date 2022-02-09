from django.shortcuts import render

from src.agencies.data.calculator import get_cities_with_pricing


def agency(request):
    cities_pricing = get_cities_with_pricing()
    context = {"cities_pricing": cities_pricing}
    return render(request, "agencies/agency.html", context)
