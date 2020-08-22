from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.conf import settings
import json
from mpr.loganalytics import test_log_analytics


class ApiUrls(TestCase):
    fixtures = ["mpr_models.json"]

    __test__ = False

    def setUp(self):
        test_log_analytics.events = []
        settings.ANALYTICS = test_log_analytics

    def __init__(self, *args, **kwargs):
        self.api_prefix = "api1"
        super(ApiUrls, self).__init__(*args, **kwargs)

    def testSearchByIngredient(self):

        client = Client()

        response = client.get(reverse(self.api_prefix + "_search_by_ingredient"), {"q" : "In"})

        self.assertEquals(len(json.loads(response.content)), 0)
        self.assertEquals(len(test_log_analytics.events), 1)
        self.assertEquals(test_log_analytics.events[0][0], "#search-by-ingredient")
        self.assertEquals(test_log_analytics.events[0][1]["query"], "In")

        response = client.get(reverse(self.api_prefix + "_search_by_ingredient"), {"q" : "Ingr"})
        self.assertEquals(len(json.loads(response.content)), 3)

        response = client.get(reverse(self.api_prefix + "_search_by_ingredient"), {"q" : "Ingredient 2"})
        self.assertEquals(len(json.loads(response.content)), 2)

    def testSearchByProduct(self):
        client = Client()

        response = client.get(reverse(self.api_prefix + "_search_by_product"), {"q" : "Pr"})
        self.assertEquals(len(json.loads(response.content)), 0)
        self.assertEquals(len(test_log_analytics.events), 1)
        self.assertEquals(test_log_analytics.events[0][0], "#search-by-product")
        self.assertEquals(test_log_analytics.events[0][1]["query"], "Pr")

        response = client.get(reverse(self.api_prefix + "_search_by_product"), {"q" : "Pro"})
        self.assertEquals(len(json.loads(response.content)), 3)

        response = client.get(reverse(self.api_prefix + "_search_by_product"), {"q" : "Product 1"})
        self.assertEquals(len(json.loads(response.content)), 1)

    def testRelatedProduct(self):
        client = Client()

        response = client.get(reverse(self.api_prefix + "_related_products"), {"product" : "1"})
        self.assertEquals(len(json.loads(response.content)), 2)
        self.assertEquals(len(test_log_analytics.events), 1)
        self.assertEquals(test_log_analytics.events[0][0], "#related")
        related_product = {
            "product": "Product 1 ABC",
            "is_generic": "Originator",
            "product_id": 1,
            "dosage_form": "Inj"
        }
        self.assertJSONEqual(json.dumps(test_log_analytics.events[0][1]), related_product)

        test_log_analytics.events = []
        response = client.get(reverse(self.api_prefix + "_related_products"), {"product" : "5"})

        self.assertEquals(len(json.loads(response.content)), 0)
        self.assertEquals(len(test_log_analytics.events), 1)
        self.assertEquals(test_log_analytics.events[0][0], "#missing-related-product")

    def testProductDetail(self):
        client = Client()

        response = client.get(reverse(self.api_prefix + "_product_detail"), {"product" : "1"})
        self.assertEquals(json.loads(response.content)["name"], "Product 1 ABC")
        self.assertEquals(len(test_log_analytics.events), 1)
        self.assertEquals(test_log_analytics.events[0][0], "#product-detail")
        product = {
            "product": "Product 1 ABC",
            "is_generic": "Originator",
            "product_id": 1,
            "dosage_form": "Inj"
        }
        self.assertJSONEqual(json.dumps(test_log_analytics.events[0][1]), product)

        test_log_analytics.events = []
        response = client.get(reverse(self.api_prefix + "_product_detail"), {"product" : "0"})
        self.assertEquals(json.loads(response.content), {})
        self.assertEquals(len(test_log_analytics.events), 1)
        self.assertEquals(test_log_analytics.events[0][0], "#missing-product-detail")
        self.assertEquals(test_log_analytics.events[0][1]["product_id"], "0")

    def testSearch(self):
        client = Client()
        response = client.get(reverse(self.api_prefix + "_search"), {"q" : "Pr"})
        self.assertEquals(len(json.loads(response.content)), 0)
        self.assertEquals(len(test_log_analytics.events), 1)

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
        self.assertEquals(len(test_log_analytics.events), 1)

        self.assertEquals(test_log_analytics.events[0][0], "#search-lite")

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
        self.assertEquals(len(test_log_analytics.events), 1)

        self.assertEquals(test_log_analytics.events[0][0], "#dump")

class TestApi(ApiUrls):
    def __init__(self, *args, **kwargs):
        super(TestApi, self).__init__(*args, **kwargs)
        self.api_prefix = "api1"

class TestApiV2(ApiUrls):
    def __init__(self, *args, **kwargs):
        super(TestApiV2, self).__init__(*args, **kwargs)
        self.api_prefix = "api2"

    def setUp(self):
        test_log_analytics.events = []
        settings.ANALYTICS = test_log_analytics

    def testSearchByProduct(self):
        client = Client()

        response = client.get(reverse(self.api_prefix + "_search_by_product"), {"nappi" : "5"})
        self.assertEquals(len(json.loads(response.content)), 0)
        self.assertEquals(len(test_log_analytics.events), 1)

        self.assertEquals(test_log_analytics.events[0][0], "#missing-product")
        self.assertEquals(test_log_analytics.events[0][1]["nappi_code"], "5")

        response = client.get(reverse(self.api_prefix + "_search_by_product"), {"nappi" : "555"})
        self.assertEquals(len(json.loads(response.content)), 0)

        test_log_analytics.events = []
        response = client.get(reverse(self.api_prefix + "_search_by_product"), {"nappi" : "111"})
        self.assertEquals(len(json.loads(response.content)), 1)
        self.assertEquals(len(test_log_analytics.events), 1)
        self.assertEquals(test_log_analytics.events[0][0], "#search-by-product")
        self.assertEquals(test_log_analytics.events[0][1]["product"], "Product 1 ABC")

    def testRelatedProduct(self):
        client = Client()

        response = client.get(reverse(self.api_prefix + "_related_products"), {"nappi" : "111"})
        self.assertEquals(len(json.loads(response.content)), 2)
        self.assertEquals(len(test_log_analytics.events), 1)
        self.assertEquals(test_log_analytics.events[0][0], "#related-product")
        self.assertEquals(test_log_analytics.events[0][1]["product"], "Product 1 ABC")

        test_log_analytics.events = []
        response = client.get(reverse(f"{self.api_prefix}_related_products"), {"nappi" : "5"})
        self.assertEquals(response.status_code, 404)

        self.assertEquals(test_log_analytics.events[0][0], "#missing-related")
        self.assertEquals(test_log_analytics.events[0][1]["nappi_code"], "5")

    def testProductDetail(self):
        client = Client()

        response = client.get(reverse(self.api_prefix + "_product_detail"), {"nappi" : "111"})
        self.assertEquals(json.loads(response.content)["name"], "Product 1 ABC")
        self.assertEquals(len(test_log_analytics.events), 1)
        self.assertEquals(test_log_analytics.events[0][0], "#product-detail")
        self.assertEquals(test_log_analytics.events[0][1]["product"], "Product 1 ABC")

        test_log_analytics.events = []
        response = client.get(reverse(self.api_prefix + "_product_detail"), {"nappi" : "0"})
        self.assertEquals(json.loads(response.content), {})
        self.assertEquals(test_log_analytics.events[0][0], "#missing-detail")
        self.assertEquals(test_log_analytics.events[0][1]["nappi_code"], "0")

    def testLastUpdated(self):
        client = Client()
        response = client.get(reverse(self.api_prefix + "_last_updated"))
        self.assertEquals(response.content, b"2014-09-29")
        self.assertEquals(len(test_log_analytics.events), 1)

        self.assertEquals(test_log_analytics.events[0][0], "#last-updated")
