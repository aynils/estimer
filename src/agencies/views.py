from django.shortcuts import render


def agency(request):
    context = {}
    return render(request, "estimer/agency.html", context)
