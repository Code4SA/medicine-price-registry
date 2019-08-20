from datetime import date
from django.test import TestCase
from django.conf import settings
from mpr import models

class TestProduct(TestCase):
    fixtures = ["mpr_models.json"]

    def setUp(self):
        self.ing1 = models.Ingredient.objects.get(pk=1)
        self.ing2 = models.Ingredient.objects.get(pk=2)
        self.p1 = models.Product.objects.get(pk=1)
        self.p2 = models.Product.objects.get(pk=2)
        self.p3 = models.Product.objects.get(pk=3)

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
        test_data = [(100, 80), (150, 100), (250, 210), (1000, 880)]

        for price, fee in test_data:
            self.p1.sep = price
            self.assertEquals(self.p1.dispensing_fee, fee)

    def testCostPerUnit(self):
        test_data = [(100, 36), (150, 50), (250, 92), (1000, 376)]

        for price, cost in test_data:
            self.p1.sep = price
            self.assertEquals(self.p1.cost_per_unit, cost)

    def testMaxFee(self):
        test_data = [(100, 180), (150, 250), (250, 460), (1000, 1880)]

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
    fixtures = ["mpr_models.json"]
    
    def setUp(self):
        self.p1 = models.Product.objects.get(pk=1)
        self.p2 = models.Product.objects.get(pk=2)
        self.p3 = models.Product.objects.get(pk=3)

    def testSearchByIngredient(self):
        ingredients = models.Product.objects.search_by_ingredient("Ingredient 1")
        self.assertEquals(len(ingredients), 3)
        self.assertTrue(self.p1 in ingredients)
        self.assertTrue(self.p2 in ingredients)
        self.assertTrue(self.p3 in ingredients)

        seps = [i.sep for i in ingredients]
        self.assertEquals(seps, sorted(seps))

        ingredients = models.Product.objects.search_by_ingredient("Ingredient 2")
        self.assertEquals(len(ingredients), 2)
        self.assertTrue(self.p1 in ingredients)
        self.assertTrue(self.p2 in ingredients)

        ingredients = models.Product.objects.search_by_ingredient("Ingredien")
        self.assertEquals(len(ingredients), 3)
        self.assertTrue(self.p1 in ingredients)
        self.assertTrue(self.p2 in ingredients)
        self.assertTrue(self.p3 in ingredients)

        ingredients = models.Product.objects.search_by_ingredient("Nothing")
        self.assertEquals(len(ingredients), 0)


    def testSearchByNappi(self):
        p = models.Product.objects.search_by_nappi("111")
        self.assertEquals(len(p), 1)
        self.assertTrue(self.p1 in p)

        p = models.Product.objects.search_by_nappi("0")
        self.assertEquals(len(p), 0)

    def testSearchByProductName(self):
        p = models.Product.objects.search_by_product_name("roduct")
        self.assertEquals(len(p), 3)

        p = models.Product.objects.search_by_product_name("Product 1")
        self.assertEquals(len(p), 1)

class TestLastUpdated(TestCase):
    fixtures = ["mpr_models.json"]

    def testLastUpdated(self):
        lu = models.LastUpdated.objects.last_updated()
        self.assertEquals(lu.update_date, date(2014, 9, 29))

