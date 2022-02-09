from django.shortcuts import render

from src.agencies.data.calculator import get_pricing_for_cities


def agency(request):
    test = get_pricing_for_cities()
    context = {"test": test}
    return render(request, "agencies/agency.html", context)
