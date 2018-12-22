from django.test import TestCase
from django.conf import settings
from mpr import models

class TestProduct(TestCase):
    def setUp(self):
        self.p1 = models.Product(
            nappi_code="nappi_code",
            regno="regno",
            name="my medicine",
            schedule="S5",
            dosage_form="Pill",
            pack_size=5,
            num_packs=1,
            sep=100,
            is_generic=True
        )

        settings.PRICE_PARAMETERS = {
            "VAT" : 2,
            "prices" : [
                (100, 0.10, 10),
                (200, 0.20, 20),
                (300, 0.30, 30),
                (float('inf'), 0.40, 40),
            ]
        }

    def testDispensingFee(self):
        test_data = [(100, 40), (150, 50), (250, 105), (1000, 440)]

        for price, fee in test_data:
            self.p1.sep = price
            self.assertEquals(self.p1.dispensing_fee, fee)

    def testCostPerUnit(self):
        test_data = [(100, 28), (150, 40), (250, 71), (1000, 288)]

        for price, cost in test_data:
            self.p1.sep = price
            self.assertEquals(self.p1.cost_per_unit, cost)

    def testMaxFee(self):
        test_data = [(100, 140), (150, 200), (250, 355), (1000, 1440)]

        for price, fee in test_data:
            self.p1.sep = price
            self.assertEquals(self.p1.max_fee, fee)

class TestProductManager(TestCase):
    def setUp(self):
        pass

    def testSearchByIngredient(self):
        return True

