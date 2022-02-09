import datetime

import pandas as pd
from django.conf import settings

from iris.data.classes import IRISData
from src.dvf.data.cities import (
    generate_chart_b64_svg,
    generate_price_evolution_text,
    get_mutations_for_iris,
    calculate_bar_heights,
    get_avg_m2_price_per_year,
)
from src.dvf.data.classes import MedianM2Price

from src.helpers.cache import cached_function
from src.iris.models import IRIS

pd.options.mode.chained_assignment = None

# from helpers.timer import timer

TODAY = datetime.date.today()
ONE_YEAR_AGO = datetime.date(year=TODAY.year - 1, month=1, day=1)
FIVE_YEARS_AGO = datetime.date(year=TODAY.year - 5, month=1, day=1)


# @timer
@cached_function(ttl=settings.CACHE_TTL_ONE_DAY)
def get_iris_data(code_iris: str) -> IRISData:
    iris = IRIS.objects.get(code_iris=code_iris)

    ventes = get_mutations_for_iris(code_iris=code_iris, date_from=FIVE_YEARS_AGO)

    avg_m2_price = get_avg_m2_price_per_year(
        types=("Maison", "Appartement"), date_from=FIVE_YEARS_AGO, ventes=ventes
    ).items()

    median_m2_prices_years = [MedianM2Price(value=price, year=year) for year, price in avg_m2_price]

    bar_heights = calculate_bar_heights(avg_m2_price=dict(avg_m2_price))

    price_evolution_text = generate_price_evolution_text(dict(avg_m2_price))

    iris_name = iris.nom_iris

    chart_b64_svg = generate_chart_b64_svg(bar_heights=bar_heights, place_name=iris_name)

    return IRISData(
        iris_name=iris_name,
        chart_b64_svg=chart_b64_svg,
        price_evolution_text=price_evolution_text,
    )
