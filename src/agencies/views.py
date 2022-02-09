from django.shortcuts import render

from src.agencies.data.calculator import get_cities_owned_by_agencies


def agency(request):
    test = get_cities_owned_by_agencies()
    context = {"test": test}
    return render(request, "agencies/agency.html", context)
