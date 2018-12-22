from django.http import HttpResponse

import apiv1
import models
import json
from loganalytics import log_analytics

def product_properties(id):
    product = models.Product.objects.get(pk=id)
    return {
        "product" : product.name,
        "product_id" : product.id,
        "dosage_form" : product.dosage_form,
        "is_generic" : product.is_generic
    }


def search_by_ingredient(request):
    q = request.GET.get("q", "").strip()
    products = apiv1.search_by_ingredient(q)
    return HttpResponse(json.dumps(products), content_type="application/json")

def search_by_product(request):
    q = request.GET.get("q", "").strip()
    products = apiv1.search_by_product(q)
    return HttpResponse(json.dumps(products), content_type="application/json")

def related_products(request):
    try:
        q = request.GET.get("product", "").strip()
        products = apiv1.related_products(q)
        response = HttpResponse(json.dumps(products), content_type="application/json")
    except models.Product.DoesNotExist:
        response = HttpResponse(json.dumps([]), content_type="application/json")

    try:
        log_analytics(request, response, "#related", product_properties(q))
    except models.Product.DoesNotExist:
        log_analytics(request, response, "#missing-product", q)

    return response
        
def product_detail(request):
    try:
        q = request.GET.get("product", "").strip()
        products = apiv1.product_detail(q)
        response = HttpResponse(json.dumps(products), content_type="application/json")
    except models.Product.DoesNotExist:
        response = HttpResponse(json.dumps({}), content_type="application/json")

    try:
        log_analytics(request, response, "#product-detail", product_properties(q))
    except models.Product.DoesNotExist:
        log_analytics(request, response, "#missing-product", q)

    return response

def search(request):
    q = request.GET.get("q", "").strip()
    products = apiv1.search(q)
    return HttpResponse(json.dumps(products), content_type="application/json")

def search_lite(request):
    q = request.GET.get("q", "").strip()
    products = apiv1.search_lite(q)
    return HttpResponse(json.dumps(products), content_type="application/json")

def dump(request):
    products = apiv1.dump()
    response = HttpResponse(json.dumps(products), content_type="application/json")

    log_analytics(request, response, "#dump", {})

    return response
