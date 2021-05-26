from django.shortcuts import render

def home(request):
    context={}
    return render(request, "estimer/home.html", context)

def mentions_legales(request):
    context={}
    return render(request, "estimer/mentions-legales.html", context)
