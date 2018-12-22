from django.test import TestCase
from django.conf import settings
from mpr import models

class TestProduct(TestCase):
    def setUp(self):
        self.ing1 = models.Ingredient(
            name="Ingredient 1",
            unit="mg",
        )
        self.ing1.save()

        self.ing2 = models.Ingredient(
            name="Ingredient 2",
            unit="mg"
        )
        self.ing2.save()

        self.p1 = models.Product(
            nappi_code="nappi_code", regno="regno", name="my medicine",
            schedule="S5", dosage_form="Pill", pack_size=5,
            num_packs=1, sep=100, is_generic=True
        )
        self.p1.save()

        self.p2 = models.Product(
            nappi_code="nappi_code2", regno="regno2", name="my medicine2",
            schedule="S7", dosage_form="Pill", pack_size=5,
            num_packs=1, sep=100, is_generic=True
        )
        self.p2.save()

        self.p3 = models.Product(
            nappi_code="nappi_code3", regno="regno3", name="my medicine3",
            schedule="S7", dosage_form="Pill", pack_size=5,
            num_packs=1, sep=100, is_generic=True
        )
        self.p3.save()

        models.ProductIngredient.objects.create(product=self.p1, ingredient=self.ing1, strength=10)
        models.ProductIngredient.objects.create(product=self.p1, ingredient=self.ing2, strength=10)
        models.ProductIngredient.objects.create(product=self.p2, ingredient=self.ing1, strength=10)
        models.ProductIngredient.objects.create(product=self.p2, ingredient=self.ing2, strength=10)
        models.ProductIngredient.objects.create(product=self.p3, ingredient=self.ing2, strength=10)

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


    def testRelatedProducts(self):
        p = self.p1.related_products
        self.assertEquals(len(p), 2)
        self.assertTrue(self.p1 in p)
        self.assertTrue(self.p2 in p)

        p = self.p2.related_products
        self.assertEquals(len(p), 2)
        self.assertTrue(self.p1 in p)
        self.assertTrue(self.p2 in p)

        p = self.p3.related_products
        self.assertEquals(len(p), 1)
        self.assertTrue(self.p3 in p)

class TestProductManager(TestCase):
    def setUp(self):
        pass

    def testSearchByIngredient(self):
        return True

