import logging

from . import models
from . import serialisers

logger = logging.getLogger(__name__)

def search_by_ingredient(query, serialiser=serialisers.serialize_products):
    
    if len(query) < 3:
        return []
    else:
        products = models.Product.objects.search_by_ingredient(query)
        return serialiser(products)

def search_by_product(query, serialiser=serialisers.serialize_products):

    if len(query) < 3:
        return []
    else:
        products = models.Product.objects.search_by_product_name(query)
        return serialiser(products)

def search(query, serialiser=serialisers.serialize_products):

    all_products = set()
    if len(query) < 3:
        products = []
    else:
        products1 = set(models.Product.objects.search_by_product_name(query))
        products2 = set(models.Product.objects.search_by_ingredient(query))
        all_products |= products1 | products2
        all_products = sorted(all_products, key=lambda x: x.sep)
        products = serialiser(all_products)

    return products

def search_lite(query):
    return search(query, serialisers.serialize_products_lite)

def related_products(product_id, serialiser=serialisers.serialize_products):
    product = models.Product.objects.get(id=product_id)
    return serialiser(product.related_products)

def dump(serialiser=serialisers.serialize_products):
    return serialiser(models.Product.objects.all())

def product_detail(product_id, serialiser=serialisers.serialize_product):
    product = models.Product.objects.get(id=product_id)
    return serialiser(product)

