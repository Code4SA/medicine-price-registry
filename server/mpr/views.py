import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.conf import settings
import names

from mpr import models
import serialisers
import logging

logger = logging.getLogger(__name__)

def get_location(ip):
    from django.contrib.gis.geoip import GeoIP
    data = {}
    if ip:
        g = GeoIP()

        data = g.city(ip)
        if data:
            city = data.get("city", None)
            country = data.get("country_name", None)
            print city, country
        else:
            data = {}
    return data
 
def log_analytics(request, event, properties):
    try:
        if settings.DEBUG: return
        import analytics
        from ipware.ip import get_ip as get_ip

        ip = get_ip(request)
        data = get_location(ip)

        name = names.get_full_name()
        uid = request.session.get("uid", name)
        analytics.init('wdfkolf5dkr7gwh12jq7')
        analytics.identify(uid, {
            "ip" : ip,
            "country" : data.get("country_name", None),
            "city" : data.get("city", None),
        })
        analytics.track(uid, event=event, properties=properties)
    except Exception, e:
        logger.exception("Error handling analytics")
    

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

    log_analytics(request, "#search", {
        "search_string" : q
    })

    all_products = set()
    if len(q) < 3:
        products = []
    else:
        products1 = set(models.Product.objects.search_by_product(q))
        products2 = set(models.Product.objects.search_by_ingredient(q))
        all_products |= products1 | products2
        all_products = sorted(all_products, key=lambda x: x.sep)
        products = serialiser(all_products)
    return HttpResponse(
        json.dumps(products, indent=4), mimetype="application/json"
    )

def search_lite(request):
    return search(request, serialisers.serialize_products_lite)

def related_products(request):
    product_id = request.GET.get("product", "").strip()
    product = get_object_or_404(models.Product, id=product_id)
    log_analytics(request, "#related", product_properties(product))

    return HttpResponse(
        json.dumps(
            serialisers.serialize_products(product.related_products), indent=4
        ), mimetype="application/json"
    )
    
def product_properties(product):
    return {
        "product" : product.name,
        "product_id" : product.id,
        "dosage_form" : product.dosage_form,
        "is_generic" : product.is_generic
    }

def product_detail(request):
    product_id = request.GET.get("product", "").strip()
    product = get_object_or_404(models.Product, id=product_id)

    log_analytics(request, "#product-detail", product_properties(product))

    return HttpResponse(
        json.dumps(
            serialisers.serialize_product(product), indent=4
        ), mimetype="application/json"
    )
