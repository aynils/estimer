from django.shortcuts import render

def home(request):
    context={}
    return render(request, "estimer/home.html", context)
