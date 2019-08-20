from django.test import TestCase
import json
from mpr import models, apiv1

def test_serialiser(products):
    return [p.pk for p in products]

def test_serialise_product(product):
    return {
        "id" : product.id,
        "name" : product.name
    }


class TestApi(TestCase):
    fixtures = ["mpr_models.json"]

    def testSearchByIngredient(self):
        products = apiv1.search_by_ingredient("In", test_serialiser)
        self.assertEquals(len(products), 0)

        products = apiv1.search_by_ingredient("Ingr", test_serialiser)
        self.assertEquals(len(products), 3)

        products = apiv1.search_by_ingredient("Ingredient 2", test_serialiser)
        self.assertEquals(len(products), 2)

    def testSearchByProduct(self):
        products = apiv1.search_by_product("Pr", test_serialiser)
        self.assertEquals(len(products), 0)

        products = apiv1.search_by_product("Pro", test_serialiser)
        self.assertEquals(len(products), 3)

        products = apiv1.search_by_product("Product 1", test_serialiser)
        self.assertEquals(len(products), 1)

    def testSearch(self):
        products = apiv1.search("So", test_serialiser)
        self.assertEquals(len(products), 0)

        products = apiv1.search("Some search", test_serialiser)
        self.assertEquals(len(products), 0)

        products = apiv1.search("Ingredient 1", test_serialiser)
        self.assertEquals(len(products), 3)

        products = apiv1.search("ABC", test_serialiser)
        self.assertEquals(len(products), 2)

    # TODO - test this better
    def testSearchLite(self):
        products = apiv1.search_lite("So")
        self.assertEquals(len(products), 0)

        products = apiv1.search_lite("Some search")
        self.assertEquals(len(products), 0)

        products = apiv1.search_lite("Ingredient 1")
        self.assertEquals(len(products), 3)

        products = apiv1.search_lite("ABC")
        self.assertEquals(len(products), 2)


    def testRelatedProducts(self):
        try:
            products = apiv1.related_products(5, test_serialiser)
            self.fail()
        except models.Product.DoesNotExist as e:
            pass

        products = apiv1.related_products(1, test_serialiser)
        self.assertEquals(len(products), 2)

        products = apiv1.related_products(3, test_serialiser)
        self.assertEquals(len(products), 1)

    def testDump(self):
       products = apiv1.dump(test_serialiser)
       self.assertEquals(len(products), 3)

    def testProductDetail(self):
        product = apiv1.product_detail(1, test_serialise_product)
        self.assertEquals(product["name"], "Product 1 ABC")

        try:
            products = apiv1.product_detail(5, test_serialise_product)
            self.fail()
        except models.Product.DoesNotExist as e:
            pass

