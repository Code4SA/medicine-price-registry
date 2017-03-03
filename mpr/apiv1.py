import json
import logging

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from mpr import models
import serialisers
from loganalytics import log_analytics

logger = logging.getLogger(__name__)


def search_by_ingredient(request):
    q = request.GET.get("q", "").strip()

    if len(q) < 3:
        products = []
    else:
        products = models.Product.objects.search_by_ingredient(q)
        products = serialisers.serialize_products(products)
    return HttpResponse(
        json.dumps(products, indent=4), mimetype="application/json"
    )

def search_by_product(request):
    q = request.GET.get("q", "").strip()

    if len(q) < 3:
        products = []
    else:
        products = models.Product.objects.search_by_product(q)
        products = serialisers.serialize_products(products)
    return HttpResponse(
        json.dumps(products, indent=4), mimetype="application/json"
    )

def search(request, serialiser=serialisers.serialize_products):
    q = request.GET.get("q", "").strip()

    all_products = set()
    if len(q) < 3:
        products = []
    else:
        products1 = set(models.Product.objects.search_by_product(q))
        products2 = set(models.Product.objects.search_by_ingredient(q))
        all_products |= products1 | products2
        all_products = sorted(all_products, key=lambda x: x.sep)
        products = serialiser(all_products)

    response = HttpResponse(
        json.dumps(products, indent=4), mimetype="application/json"
    )

    log_analytics(request, response, "#search", {
        "search_string" : q
    })

    return response

def search_lite(request):
    return search(request, serialisers.serialize_products_lite)

def related_products(request):
    product_id = request.GET.get("product", "").strip()
    product = get_object_or_404(models.Product, id=product_id)

    response = HttpResponse(
        json.dumps(
            serialisers.serialize_products(product.related_products), indent=4
        ), mimetype="application/json"
    )

    log_analytics(request, response, "#related", product_properties(product))
    return response

def product_properties(product):
    return {
        "product" : product.name,
        "product_id" : product.id,
        "dosage_form" : product.dosage_form,
        "is_generic" : product.is_generic
    }

def dump(request):

    response = HttpResponse(
        json.dumps(
            serialisers.serialize_products(models.Product.objects.all()), indent=4
        ), mimetype="application/json"
    )
    log_analytics(request, response, "#dump", {})
    return response

def product_detail(request):
    product_id = request.GET.get("product", "").strip()
    product = get_object_or_404(models.Product, id=product_id)

    response = HttpResponse(
        json.dumps(
            serialisers.serialize_product(product), indent=4
        ), mimetype="application/json"
    )

    log_analytics(request, response, "#product-detail", product_properties(product))
    return response

