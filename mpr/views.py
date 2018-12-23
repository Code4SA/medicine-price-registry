from django.http import HttpResponse

import apiv1, apiv2
import models
import json
from loganalytics import log_analytics

def product_properties(product_code):
    product = None
    if type(product_code) in (str, unicode):
        products = models.Product.objects.filter(pk=product_code)
        if len(products) > 0:
            product = products[0]
        else:
            products = models.Product.objects.filter(nappi_code=product_code)
            if len(products) > 0:
                product = products[0]
               
    if not product:
        return {}
    else:
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

def v2_related_products(request):
    try:
        q = request.GET.get("nappi", "").strip()
        products = apiv2.related_products(q)
        response = HttpResponse(json.dumps(products), content_type="application/json")
    except models.Product.DoesNotExist:
        response = HttpResponse(json.dumps([]), content_type="application/json")

    try:
        p = models.Product.objects.get(nappi_code=q)
        log_analytics(request, response, "#related", product_properties(q))
    except models.Product.DoesNotExist:
        log_analytics(request, response, "#missing-product", q)

    return response

def v2_product_detail(request):
    product = None
    try:
        nappi_code = request.GET.get("nappi", "").strip()
        products = apiv2.product_detail(nappi_code)
        response = HttpResponse(json.dumps(products), content_type="application/json")
    except models.Product.DoesNotExist:
        response = HttpResponse(json.dumps({}), content_type="application/json")

    if product:
        log_analytics(request, response, "#product-detail", product_properties(q))
    else:
        log_analytics(request, response, "#missing-product", nappi_code)

    return response

def v2_search_by_product(request):
    nappi_code = request.GET.get("nappi", "").strip()
    products = apiv2.search_by_product(nappi_code)
    response = HttpResponse(json.dumps(products), content_type="application/json")

    if len(products) == 1:
        log_analytics(request, response, "#search-by-product", product_properties(nappi_code))
    elif len(products) > 1:
        log_analytics(request, response, "#search-by-product-more-than-one", product_properties(nappi_code))
    else:
        log_analytics(request, response, "#missing-product", nappi_code)

    return response
    
def v2_search(request):
    q = request.GET.get("q", "").strip()
    products = apiv2.search(q)
    response =  HttpResponse(json.dumps(products), content_type="application/json")

    log_analytics(request, response, "#search", {
        "search_string" : q
    })

    return response

def v2_search_lite(request):
    q = request.GET.get("q", "").strip()
    products = apiv2.search_lite(q)
    response =  HttpResponse(json.dumps(products), content_type="application/json")

    log_analytics(request, response, "#search_lite", {
        "search_string" : q
    })

    return response

def v2_last_updated(request):
    last_updated = apiv2.last_updated()
    response =  HttpResponse(last_updated, content_type="application/json")
    log_analytics(request, response, "#last-updated")
    return response
