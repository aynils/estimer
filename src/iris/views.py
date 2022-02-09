from django.http import JsonResponse

from src.iris.data.iris import get_iris_data


def get_data_for_iris(request) -> JsonResponse:
    code_iris = request.GET.get("iris")
    iris_data = get_iris_data(code_iris=code_iris)
    data = {
        "iris": code_iris,
        "price_evolution_text": iris_data.price_evolution_text,
        "chart_b64_svg": iris_data.chart_b64_svg,
        "iris_name": iris_data.iris_name,
    }
    return JsonResponse(data)
