import datetime

from django.test import TestCase
from dvf.aggregator.data_import import import_data
from dvf.models import ValeursFoncieres


# Create your tests here.
class TestImport(TestCase):
    def setUp(self):
        import_data(2020)

    def test_import_2020_data(self):
        data = ValeursFoncieres.objects.filter(
            date_mutation__gte=datetime.date(year=2020, month=1, day=1)
        ).all()
        assert data
