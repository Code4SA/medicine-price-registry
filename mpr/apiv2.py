import json
import logging

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

from .import models
from .import serialisers
from .loganalytics import log_analytics
from .packageinserts import packageinserts

logger = logging.getLogger(__name__)

def search_by_product(request):
    q = request.GET.get("nappi", "").strip()

    if len(q) < 3:
        products = []
    else:
        products = models.Product.objects.search_by_nappi(q)
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
        products0 = set(models.Product.objects.search_by_nappi(q))
        products1 = set(models.Product.objects.search_by_product_name(q))
        products2 = set(models.Product.objects.search_by_ingredient(q))
        all_products |= products0 | products1 | products2
        all_products = sorted(all_products, key=lambda x: x.sep)
        products = serialiser(all_products)

    response = HttpResponse(
        json.dumps(products, indent=4), content_type="application/json"
    )

    log_analytics(request, response, "#search", {
        "search_string" : q
    })

    return response

def search_lite(request):
    return search(request, serialisers.serialize_products_lite)

def related_products(request):
    nappi_code = request.GET.get("nappi", "").strip()
    product = get_object_or_404(models.Product, nappi_code=nappi_code)

    response = HttpResponse(
        json.dumps(
            serialisers.serialize_products(product.related_products), indent=4
        ), content_type="application/json"
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

def product_detail(request):
    nappi_code = request.GET.get("nappi", "").strip()
    product = get_object_or_404(models.Product, nappi_code=nappi_code)
    js = serialisers.serialize_product(product)
    if js["regno"] in packageinserts:
        js["insert_url"] = packageinserts[js["regno"]]

    response = HttpResponse(
        json.dumps(js, indent=4), content_type="application/json")

    log_analytics(request, response, "#product-detail", product_properties(product))
    return response


def last_updated(request):
    last_updated_date = models.LastUpdated.objects.last_updated().update_date.isoformat()
    response = HttpResponse(last_updated_date, content_type="application/json")
    log_analytics(request, response, "#last-updated")
    return response
