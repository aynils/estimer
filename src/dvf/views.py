from django.shortcuts import render

# Create your views here.
def city(request, slug):
    context = {
        "slug":slug
    }

    return render(request, "dvf/city.html", context)
