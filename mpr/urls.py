from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from mpr.models import LastUpdated
from mpr import views

from django.contrib import admin
import apiv1, apiv2
admin.autodiscover()

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        try:
            last_updated = LastUpdated.objects.all().order_by('-update_date')[0]
            context['last_updated'] = last_updated
        except:
            context['last_updated'] = u"Never"
        return context

urlpatterns = [
    url(r'^$', IndexView.as_view(template_name="index.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),

    url(r"^api/related$", views.related_products, name="api_related_products"),
    url(r"^api/detail$", views.product_detail, name="api_product_detail"),
    url(r"^api/search/by_product$", views.search_by_product, name="api_search_by_product"),
    url(r"^api/search/by_ingredient$", views.search_by_ingredient, name="api_search_by_ingredient"),
    url(r"^api/search$", views.search, name="api_search"),
    url(r"^api/search-lite$", views.search_lite, name="api_search_lite"),
    url(r"^api/dump$", views.dump, name="api_dump"),

    url(r"^api/v1/related$", views.related_products, name="api1_related_products"),
    url(r"^api/v1/detail$", views.product_detail, name="api1_product_detail"),
    url(r"^api/v1/search/by_product$", views.search_by_product, name="api1_search_by_product"),
    url(r"^api/v1/search/by_ingredient$", views.search_by_ingredient, name="api1_search_by_ingredient"),
    url(r"^api/v1/search$", views.search, name="api1_search"),
    url(r"^api/v1/search-lite$", views.search_lite, name="api1_search_lite"),
    url(r"^api/v1/dump$", views.dump, name="api1_dump"),

    url(r"^api/v2/related$", apiv2.related_products, name="api2_related_products"),
    url(r"^api/v2/detail$", apiv2.product_detail, name="api2_product_detail"),
    url(r"^api/v2/search/by_product$", apiv2.search_by_product, name="api2_search_by_product"),
    url(r"^api/v2/search$", apiv2.search, name="api2_search"),
    url(r"^api/v2/search-lite$", apiv2.search_lite, name="api2_search_lite"),
    url(r"^api/v2/last-updated$", apiv2.last_updated, name="api2_last_updated"),

    # currently still using v1 methods since there hasn't been a change
    url(r"^api/v2/dump$", apiv1.dump, name="api2_dump"),
    url(r"^api/v2/search/by_ingredient$", apiv1.search_by_ingredient, name="api2_search_by_ingredient"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
