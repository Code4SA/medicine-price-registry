import json

from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings

from . import apiv1, apiv2
from . import models
from .loganalytics import log_analytics

def product_properties(product_code):
    product = None
    if type(product_code) == str:
        products = models.Product.objects.filter(pk=product_code)
        if len(products) > 0:
            product = products[0]
        else:
            products = models.Product.objects.filter(nappi_code=product_code)
            if len(products) > 0:
                product = products[0]
               
    if not product:
        raise models.Product.DoesNotExist()
    else:
        return {
            "product" : product.name,
            "product_id" : product.id,
            "dosage_form" : product.dosage_form,
            "is_generic" : product.is_generic
        }

class AnalyticsMixin(object):
    def get_analytics_logger(self):
        return settings.ANALYTICS

class SearchByIngredientView(View, AnalyticsMixin):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q", "").strip()
        products = apiv1.search_by_ingredient(q)

        response = HttpResponse(json.dumps(products), content_type="application/json")
        log_analytics = self.get_analytics_logger()
        log_analytics(request, response, "#search-by-ingredient", query=q)
        return response

class SearchByProductView(View, AnalyticsMixin):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q", "").strip()
        products = apiv1.search_by_product(q)
        response = HttpResponse(json.dumps(products), content_type="application/json")

        log_analytics = self.get_analytics_logger()
        log_analytics(request, response, "#search-by-product", query=q)
        return response

class RelatedProductsView(View, AnalyticsMixin):
    def get(self, request, *args, **kwargs):
        try:
            q = request.GET.get("product", "").strip()
            products = apiv1.related_products(q)
            response = HttpResponse(json.dumps(products), content_type="application/json")
        except models.Product.DoesNotExist:
            response = HttpResponse(json.dumps([]), content_type="application/json")

        log_analytics = self.get_analytics_logger()
        try:
            log_analytics(request, response, "#related", **product_properties(q))
        except models.Product.DoesNotExist:
            log_analytics(request, response, "#missing-related-product", product_id=q)

        return response
        
class ProductDetailView(View, AnalyticsMixin):
    def get(self, request, *args, **kwargs):
        try:
            q = request.GET.get("product", "").strip()
            products = apiv1.product_detail(q)
            response = HttpResponse(json.dumps(products), content_type="application/json")
        except models.Product.DoesNotExist:
            response = HttpResponse(json.dumps({}), content_type="application/json")

        log_analytics = self.get_analytics_logger()
        try:
            log_analytics(request, response, "#product-detail", **product_properties(q))
        except models.Product.DoesNotExist:
            log_analytics(request, response, "#missing-product-detail", product_id=q)

        return response

class SearchView(View, AnalyticsMixin):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q", "").strip()
        products = apiv1.search(q)
        response =  HttpResponse(json.dumps(products), content_type="application/json")
        log_analytics = self.get_analytics_logger()
        log_analytics(request, response, "#search", query=q)
        return response

class SearchLiteView(View, AnalyticsMixin):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q", "").strip()
        products = apiv1.search_lite(q)
        response =  HttpResponse(json.dumps(products), content_type="application/json")
        log_analytics = self.get_analytics_logger()
        log_analytics(request, response, "#search-lite", query=q)
        return response

class DumpView(View, AnalyticsMixin):
    def get(self, request, *args, **kwargs):
        products = apiv1.dump()
        response = HttpResponse(json.dumps(products), content_type="application/json")

        log_analytics = self.get_analytics_logger()
        log_analytics(request, response, "#dump")

        return response

class V2RelatedProductsView(View, AnalyticsMixin):
    def get(self, request, *args, **kwargs):
        try:
            q = request.GET.get("nappi", "").strip()
            products = apiv2.related_products(q)
            response = HttpResponse(json.dumps(products), content_type="application/json")
        except models.Product.DoesNotExist:
            response = HttpResponse(json.dumps([]), content_type="application/json")

        log_analytics = self.get_analytics_logger()
        try:
            p = models.Product.objects.get(nappi_code=q)
            log_analytics(request, response, "#related-product", **product_properties(q))
        except models.Product.DoesNotExist:
            log_analytics(request, response, "#missing-related", nappi_code=q)

        return response

class V2ProductDetailView(View, AnalyticsMixin):
    def get(self, request, *args, **kwargs):

        product = None
        try:
            nappi_code = request.GET.get("nappi", "").strip()
            product = apiv2.product_detail(nappi_code)
            response = HttpResponse(json.dumps(product), content_type="application/json")
        except models.Product.DoesNotExist:
            response = HttpResponse(json.dumps({}), content_type="application/json")

        log_analytics = self.get_analytics_logger()
        if product:
            log_analytics(request, response, "#product-detail", **product_properties(nappi_code))
        else:
            log_analytics(request, response, "#missing-detail", nappi_code=nappi_code)

        return response

class V2SearchByProduct(View, AnalyticsMixin):
    def get(self, request, *args, **kwargs):
        nappi_code = request.GET.get("nappi", "").strip()
        products = apiv2.search_by_product(nappi_code)
        response = HttpResponse(json.dumps(products), content_type="application/json")

        log_analytics = self.get_analytics_logger()
        if len(products) == 1:
            log_analytics(request, response, "#search-by-product", **product_properties(nappi_code))
        elif len(products) > 1:
            log_analytics(request, response, "#search-by-product-more-than-one", **product_properties(nappi_code))
        else:
            log_analytics(request, response, "#missing-product", nappi_code=nappi_code)

        return response
    
class V2SearchView(View, AnalyticsMixin):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q", "").strip()
        products = apiv2.search(q)
        response =  HttpResponse(json.dumps(products), content_type="application/json")
        log_analytics = self.get_analytics_logger()
        log_analytics(request, response, "#search", query=q)
        return response

class V2SearchLiteView(View, AnalyticsMixin):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q", "").strip()
        products = apiv2.search_lite(q)
        response =  HttpResponse(json.dumps(products), content_type="application/json")
        log_analytics = self.get_analytics_logger()
        log_analytics(request, response, "#search-lite", query=q)
        return response

class LastUpdatedView(View, AnalyticsMixin):
    def get(self, request, *args, **kwargs):
        last_updated = apiv2.last_updated()
        response =  HttpResponse(last_updated, content_type="application/json")
        log_analytics = self.get_analytics_logger()
        log_analytics(request, response, "#last-updated")
        return response
