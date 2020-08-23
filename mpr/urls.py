from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path

from . import apiv1, apiv2
from . import views
from .models import LastUpdated

admin.autodiscover()

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        try:
            last_updated = LastUpdated.objects.all().order_by('-update_date')[0]
            context['last_updated'] = last_updated
            context['price_parameters'] = settings.PRICE_PARAMETERS
            context['latest_gazette'] = settings.LATEST_GAZETTE
        except:
            context['last_updated'] = u"Never"
        return context

urlpatterns = [
    url(r'^$', IndexView.as_view(template_name="index.html"), name="home"),
    path("admin/", admin.site.urls),

    url(r"^api/related$", views.RelatedProductsView.as_view(), name="api_related_products"),
    url(r"^api/detail$", views.ProductDetailView.as_view(), name="api_product_detail"),
    url(r"^api/search/by_product$", views.SearchByProductView.as_view(), name="api_search_by_product"),
    url(r"^api/search/by_ingredient$", views.SearchByIngredientView.as_view(), name="api_search_by_ingredient"),
    url(r"^api/search$", views.SearchView.as_view(), name="api_search"),
    url(r"^api/search-lite$", views.SearchLiteView.as_view(), name="api_search_lite"),
    url(r"^api/dump$", views.DumpView.as_view(), name="api_dump"),

    url(r"^api/v1/related$", views.RelatedProductsView.as_view(), name="api1_related_products"),
    url(r"^api/v1/detail$", views.ProductDetailView.as_view(), name="api1_product_detail"),
    url(r"^api/v1/search/by_product$", views.SearchByProductView.as_view(), name="api1_search_by_product"),
    url(r"^api/v1/search/by_ingredient$", views.SearchByIngredientView.as_view(), name="api1_search_by_ingredient"),
    url(r"^api/v1/search$", views.SearchView.as_view(), name="api1_search"),
    url(r"^api/v1/search-lite$", views.SearchLiteView.as_view(), name="api1_search_lite"),
    url(r"^api/v1/dump$", views.DumpView.as_view(), name="api1_dump"),

    url(r"^api/v2/related$", views.V2RelatedProductsView.as_view(), name="api2_related_products"),
    url(r"^api/v2/detail$", views.V2ProductDetailView.as_view(), name="api2_product_detail"),
    url(r"^api/v2/search/by_product$", views.V2SearchByProduct.as_view(), name="api2_search_by_product"),
    url(r"^api/v2/search$", views.V2SearchView.as_view(), name="api2_search"),
    url(r"^api/v2/search-lite$", views.V2SearchLiteView.as_view(), name="api2_search_lite"),
    url(r"^api/v2/last-updated$", views.LastUpdatedView.as_view(), name="api2_last_updated"),

    # currently still using v1 methods since there hasn't been a change
    url(r"^api/v2/dump$", views.DumpView.as_view(), name="api2_dump"),
    url(r"^api/v2/search/by_ingredient$", views.SearchByIngredientView.as_view(), name="api2_search_by_ingredient"),

    # API V3 - using some old api calls as they haven't changed
    url(r"^api/v3/related$", views.V2RelatedProductsView.as_view(), name="api3_related_products"),
    url(r"^api/v3/detail$", views.V3ProductDetailView.as_view(), name="api3_product_detail"),
    url(r"^api/v3/search/by_product$", views.V2SearchByProduct.as_view(), name="api3_search_by_product"),
    url(r"^api/v3/search$", views.V2SearchView.as_view(), name="api3_search"),
    url(r"^api/v3/search-lite$", views.V2SearchLiteView.as_view(), name="api3_search_lite"),
    url(r"^api/v3/last-updated$", views.LastUpdatedView.as_view(), name="api3_last_updated"),

    # currently still using v1 methods since there hasn't been a change
    url(r"^api/v3/dump$", views.DumpView.as_view(), name="api3_dump"),
    url(r"^api/v3/search/by_ingredient$", views.SearchByIngredientView.as_view(), name="api3_search_by_ingredient"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
