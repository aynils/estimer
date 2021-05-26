import datetime

from dvf.aggregator.data_import import import_data
from dvf.models import ValeursFoncieres
from dvf.data.cities import get_simple_sales, get_city_data, get_all_cities
import unittest
import logging

logger = logging.getLogger(__name__)


# Create your tests here.
class TestCommunes(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        logger.info('Start import data for 2020 ...')
        data_count = ValeursFoncieres.objects.filter(
            date_mutation__gte=datetime.date(year=2020, month=1, day=1)
        ).count()
        if data_count != 2459560:
            import_data(2020)
            logger.info('Data for 2020 imported successfuly!')
        else:
            logger.info('Data for 2020 already there!')

    def test_import_2020_data(self):
        data_count = ValeursFoncieres.objects.filter(
            date_mutation__gte=datetime.date(year=2020, month=1, day=1)
        ).count()
        logger.info(f"{data_count} lines in data for 2020")
        assert data_count == 2459560

    def test_raw_data_montpellier(self):
        raw_city_data = get_simple_sales(
            code_commune="34172",
            types=('Appartement', 'Maison'),
            date_from=datetime.date(year=2020, month=1, day=1)
        )
        logger.info(f"{len(raw_city_data)} lines for Montpellier")
        assert len(raw_city_data) == 1088

    def test_city_data_montpellier(self):
        city_data = get_city_data(
            code_commune="34172",
        )
        # logger.info(f"Data for Montpellier: {city_data}")
        assert city_data.median_m2_price_appartement.year == 2020
        assert city_data.median_m2_price_appartement.value == 3004
        assert city_data.median_m2_price_maison.year == 2020
        assert city_data.median_m2_price_maison.value == 3823

    def test_get_all_cities(self):
        all_cities = get_all_cities()
        logger.info(f"Found {len(all_cities)} cities")
        assert len(all_cities) == 31076
