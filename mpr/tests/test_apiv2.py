import json

from django.test import TestCase
from django.http import Http404
from mpr import models, apiv2

def test_serialiser(products):
    return [p.pk for p in products]

class TestApiV2(TestCase):
    fixtures = ["mpr_models.json"]

    def testSearchByProduct(self):
        products = apiv2.search_by_product("5", test_serialiser)
        self.assertEquals(len(products), 0)

        products = apiv2.search_by_product("555", test_serialiser)
        self.assertEquals(len(products), 0)

        products = apiv2.search_by_product("111", test_serialiser)
        self.assertEquals(len(products), 1)

        products = apiv2.search_by_product("222", test_serialiser)
        self.assertEquals(len(products), 1)

    def testSearch(self):
        products = apiv2.search("So", test_serialiser)
        self.assertEquals(len(products), 0)

        products = apiv2.search("Some search", test_serialiser)
        self.assertEquals(len(products), 0)

        products = apiv2.search("Ingredient 1", test_serialiser)
        self.assertEquals(len(products), 3)

        products = apiv2.search("ABC", test_serialiser)
        self.assertEquals(len(products), 2)

        products = apiv2.search("111", test_serialiser)
        self.assertEquals(len(products), 1)

    def testSearchLite(self):
        products = apiv2.search_lite("So", test_serialiser)
        self.assertEquals(len(products), 0)

        products = apiv2.search_lite("Some search", test_serialiser)
        self.assertEquals(len(products), 0)

        products = apiv2.search_lite("Ingredient 1", test_serialiser)
        self.assertEquals(len(products), 3)

        products = apiv2.search_lite("ABC", test_serialiser)
        self.assertEquals(len(products), 2)

    def testRelatedProducts(self):
        try:
            products = apiv2.related_products(5, test_serialiser)
            self.fail()
        except Http404 as e:
            pass

        products = apiv2.related_products(222, test_serialiser)
        self.assertEquals(len(products), 2)

        products = apiv2.related_products(333, test_serialiser)
        self.assertEquals(len(products), 1)
