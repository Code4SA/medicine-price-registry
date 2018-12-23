from django.test import TestCase
from mpr import serialisers
from mpr import models
import json

product1_json = {
    "schedule": "S4",
    "is_generic": "Originator",
    "regno": "REGNO2",
    "pack_size": 5.0,
    "dispensing_fee": "R 40.00",
    "id": 1,
    "num_packs": 1,
    "name": "Product 1 ABC",
    "ingredients": [
        {
            "strength": 20,
            "name": "Ingredient 1",
            "unit": "mg"
        },
        {
            "strength": 20,
            "name": "Ingredient 2 ABC",
            "unit": "mg"
        }
    ],
    "sep": "R 140.00",
    "cost_per_unit": "R 28.00",
    "nappi_code": "111",
    "dosage_form": "injection"
}

product1_lite_json = {
    "dosage_form": "injection",
    "sep": "R 140.00",
    "id": 1,
    "nappi_code": "111",
    "name": "Product 1 ABC"
}

class TestSerialisers(TestCase):
    fixtures = ["mpr_models.json"]

    def testAscurrency(self):
        self.assertEquals(serialisers.as_currency(10), "R 10.00")
        self.assertEquals(serialisers.as_currency(1000), "R 1000.00")
        self.assertEquals(serialisers.as_currency("not a number"), "-")
        self.assertEquals(serialisers.as_currency(None), "-")
        self.assertEquals(serialisers.as_currency(-1000), "R -1000.00")

    def testIntOrFloat(self):
        self.assertEquals(serialisers.int_or_float(1), 1)
        self.assertEquals(serialisers.int_or_float(None), "-")
        self.assertEquals(serialisers.int_or_float("Not a number"), "-")


    def testSerialiseIngredient(self):
        ingredient = models.Ingredient.objects.all()[0]
        js = serialisers.serialize_ingredient(ingredient, 200) 
        self.assertTrue("name" in js and js["name"] == "Ingredient 1")
        self.assertTrue("unit" in js and js["unit"] == "mg")
        self.assertTrue("strength" in js and js["strength"] == 200)
        
    def testSerialiseProduct(self):
        product = models.Product.objects.all()[0]
        js = serialisers.serialize_product(product) 

        self.assertJSONEqual(json.dumps(js), product1_json)

    def testSerialiseProducts(self):
        products = models.Product.objects.all()
        js = serialisers.serialize_products(products) 
        self.assertEquals(len(js), 3)
        self.assertJSONEqual(json.dumps(js[0]), product1_json)

    def testSerialiseProductLite(self):
        product = models.Product.objects.all()[0]
        js = serialisers.serialize_product_lite(product) 
        self.assertJSONEqual(json.dumps(js), product1_lite_json)

    def testSerialiseProductsLite(self):
        products = models.Product.objects.all()
        js = serialisers.serialize_products_lite(products) 
        self.assertEquals(len(js), 3)
        self.assertJSONEqual(json.dumps(js[0]), product1_lite_json)
