from django.shortcuts import render


def agency(request):
    context = {}
    return render(request, "agencies/agency.html", context)
