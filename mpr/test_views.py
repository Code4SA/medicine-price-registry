from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
import json

class ApiUrls(TestCase):
    fixtures = ["mpr_models.json"]

    __test__ = False

    def __init__(self, *args, **kwargs):
        self.api_prefix = "api1"
        super(ApiUrls, self).__init__(*args, **kwargs)

    def testSearchByIngredient(self):

        client = Client()

        response = client.get(reverse(self.api_prefix + "_search_by_ingredient"), {"q" : "In"})
        self.assertEquals(len(json.loads(response.content)), 0)

        response = client.get(reverse(self.api_prefix + "_search_by_ingredient"), {"q" : "Ingr"})
        self.assertEquals(len(json.loads(response.content)), 3)

        response = client.get(reverse(self.api_prefix + "_search_by_ingredient"), {"q" : "Ingredient 2"})
        self.assertEquals(len(json.loads(response.content)), 2)

    def testSearchByProduct(self):
        client = Client()

        response = client.get(reverse(self.api_prefix + "_search_by_product"), {"q" : "Pr"})
        self.assertEquals(len(json.loads(response.content)), 0)

        response = client.get(reverse(self.api_prefix + "_search_by_product"), {"q" : "Pro"})
        self.assertEquals(len(json.loads(response.content)), 3)

        response = client.get(reverse(self.api_prefix + "_search_by_product"), {"q" : "Product 1"})
        self.assertEquals(len(json.loads(response.content)), 1)

    def testRelatedProduct(self):
        client = Client()

        response = client.get(reverse(self.api_prefix + "_related_products"), {"product" : "1"})
        self.assertEquals(len(json.loads(response.content)), 2)

        response = client.get(reverse(self.api_prefix + "_related_products"), {"product" : "5"})
        self.assertEquals(len(json.loads(response.content)), 0)

    def testProductDetail(self):
        client = Client()

        response = client.get(reverse(self.api_prefix + "_product_detail"), {"product" : "1"})
        self.assertEquals(json.loads(response.content)["name"], "Product 1 ABC")

        response = client.get(reverse(self.api_prefix + "_product_detail"), {"product" : "0"})
        self.assertEquals(json.loads(response.content), {})

    def testSearch(self):
        client = Client()

        response = client.get(reverse(self.api_prefix + "_search"), {"q" : "Pr"})
        self.assertEquals(len(json.loads(response.content)), 0)

        response = client.get(reverse(self.api_prefix + "_search"), {"q" : "Prod"})
        self.assertEquals(len(json.loads(response.content)), 3)

        response = client.get(reverse(self.api_prefix + "_search"), {"q" : "ABC"})
        self.assertEquals(len(json.loads(response.content)), 2)
        js = json.loads(response.content)
        names = [j["name"] for j in js]
        self.assertTrue("Product 1 ABC" in names)
        self.assertTrue("Product 2" in names)

    def testSearchLite(self):
        client = Client()

        response = client.get(reverse(self.api_prefix + "_search_lite"), {"q" : "Pr"})
        self.assertEquals(len(json.loads(response.content)), 0)

        response = client.get(reverse(self.api_prefix + "_search_lite"), {"q" : "Prod"})
        self.assertEquals(len(json.loads(response.content)), 3)

        response = client.get(reverse(self.api_prefix + "_search_lite"), {"q" : "ABC"})
        self.assertEquals(len(json.loads(response.content)), 2)
        js = json.loads(response.content)
        names = [j["name"] for j in js]
        self.assertTrue("Product 1 ABC" in names)
        self.assertTrue("Product 2" in names)

    def testDump(self):
        client = Client()

        response = client.get(reverse(self.api_prefix + "_dump"))
        self.assertEquals(len(json.loads(response.content)), 3)

class TestApi(ApiUrls):
    def __init__(self, *args, **kwargs):
        super(TestApi, self).__init__(*args, **kwargs)
        self.api_prefix = "api1"
