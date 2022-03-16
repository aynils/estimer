from django.shortcuts import render


def home(request):
    context = {}
    return render(request, "estimer/home.html", context)


def mentions_legales(request):
    context = {}
    return render(request, "estimer/mentions-legales.html", context)


def cgv(request):
    context = {}
    return render(request, "estimer/cgv.html", context)


def page_404(request, exception):
    return render(request, "dvf/404.html", status=404)


def page_500(request):
    return render(request, "dvf/500.html", status=500)
