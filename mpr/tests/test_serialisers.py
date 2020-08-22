from copy import deepcopy
from django.test import TestCase
from mpr import serialisers
from mpr import models
import json

ingredient1_json = {
    "strength": 200,
    "name": "Ingredient 1",
    "unit": "mg"
}

product1_json = {
    "schedule": "S4",
    "is_generic": "Originator",
    "regno": "REGNO2",
    "pack_size": 5.0,
    "dispensing_fee": "R 80.00",
    "id": 1,
    "num_packs": 1,
    "name": "Product 1 ABC",
    "number_of_generics": 2,
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
    "sep": "R 180.00",
    "cost_per_unit": "R 36.00",
    "nappi_code": "111",
    "dosage_form": "injection"
}

product1_apiv3_json = deepcopy(product1_json)
product1_apiv3_json["sep"] = "R 100.00"
product1_apiv3_json.update({
    "max_cost_per_unit": "R 36.00",
    "max_price": "R 180.00",
    "min_cost_per_unit": "R 20.00",
    "min_price": "R 100.00",
})

product1_lite_json = {
    "dosage_form": "injection",
    "sep": "R 180.00",
    "id": 1,
    "nappi_code": "111",
    "name": "Product 1 ABC",
    "number_of_generics": 2
}

product1_lite_apiv3_json = deepcopy(product1_lite_json)
product1_lite_apiv3_json["sep"] = "R 100.00"

class TestSerialisers(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSerialisers, self).__init__(*args, **kwargs)
        self.maxDiff = None

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
        self.assertJSONEqual(json.dumps(js), ingredient1_json)
        
    def testSerialiseProduct(self):
        product = models.Product.objects.all()[0]
        js = serialisers.serialize_product(product) 

        self.assertJSONEqual(json.dumps(js), product1_json)

    def testSerialiseProductAPIV3(self):
        product = models.Product.objects.all()[0]
        js = serialisers.serialize_product_apiv3(product) 

        self.assertJSONEqual(json.dumps(js), product1_apiv3_json)

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
        self.assertEquals(products.count(), 3)

        js = serialisers.serialize_products_lite(products) 
        self.assertEquals(len(js), 3)
        print(js[0])
        self.assertJSONEqual(json.dumps(js[0]), product1_lite_json)
