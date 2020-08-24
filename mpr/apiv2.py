import json
import logging

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, get_list_or_404

from .import models
from .import serialisers
from .loganalytics import log_analytics
from .packageinserts import packageinserts

logger = logging.getLogger(__name__)

def search_by_product(query, serialiser=serialisers.serialize_products):

    if len(query) < 3:
        return []
    else:
        products = models.Product.objects.search_by_nappi(query)
        return serialiser(products)

def search(query, serialiser=serialisers.serialize_products):
    all_products = set()
    if len(query) < 3:
        products = []
    else:
        products0 = set(models.Product.objects.search_by_nappi(query))
        products1 = set(models.Product.objects.search_by_product_name(query))
        products2 = set(models.Product.objects.search_by_ingredient(query))
        all_products |= products0 | products1 | products2
        all_products = sorted(all_products, key=lambda x: x.sep)
        products = serialiser(all_products)
    return products

def search_lite(query, serialiser=serialisers.serialize_products):
    return search(query, serialisers.serialize_products_lite)

def related_products(nappi_code, serialiser=serialisers.serialize_products):
    products = get_list_or_404(models.Product, nappi_code=nappi_code)
    product = products[0]
    return serialiser(product.related_products)

def product_properties(product):
    return {
        "product" : product.name,
        "product_id" : product.id,
        "dosage_form" : product.dosage_form,
        "is_generic" : product.is_generic
    }

def product_detail(nappi_code, serialiser=serialisers.serialize_product):
    try:
        product = models.Product.objects.filter(nappi_code=nappi_code).first()
        if product is None:
            raise models.Product.DoesNotExist()

        js = serialiser(product)
        if js["regno"] in packageinserts:
            js["insert_url"] = packageinserts[js["regno"]]
        return js
    except models.Product.DoesNotExist:
        return {}

def last_updated():
    last_updated_date = models.LastUpdated.objects.last_updated().update_date.isoformat()
    return last_updated_date
