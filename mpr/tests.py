from django.test import TestCase
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

        pass

    def testDispensingFee(self):
        self.assertAlmostEquals(self.p1.dispensing_fee, 65.837, 2)

    def testCostPerUnit(self):
        self.assertAlmostEquals(self.p1.cost_per_unit, 33.1675, 2)

    def testMaxFee(self):
        self.assertAlmostEquals(self.p1.max_fee, 165.837, 2)
        

class TestProductManager(TestCase):
    def setUp(self):
        pass

    def testSearchByIngredient(self):
        return True

