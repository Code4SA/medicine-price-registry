import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from mpr import models
import serialisers

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

def search(request):
    q = request.GET.get("q", "").strip()

    all_products = set()
    if len(q) < 3:
        products = []
    else:
        products1 = set(models.Product.objects.search_by_product(q))
        products2 = set(models.Product.objects.search_by_ingredient(q))
        all_products |= products1 | products2
        all_products = sorted(all_products, key=lambda x: x.sep)
        products = serialisers.serialize_products(all_products)
    return HttpResponse(
        json.dumps(products, indent=4), mimetype="application/json"
    )

def related_products(request):
    product_id = request.GET.get("product", "").strip()
    product = get_object_or_404(models.Product, id=product_id)

    return HttpResponse(
        json.dumps(
            serialisers.serialize_products(product.related_products), indent=4
        ), mimetype="application/json"
    )
    
def product_detail(request):
    product_id = request.GET.get("product", "").strip()
    product = get_object_or_404(models.Product, id=product_id)

    return HttpResponse(
        json.dumps(
            serialisers.serialize_product(product), indent=4
        ), mimetype="application/json"
    )
