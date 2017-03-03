from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from mpr.models import LastUpdated

from django.contrib import admin
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

urlpatterns = patterns("",
    url(r'^$', IndexView.as_view(template_name="index.html"), name="home"),
    url(r"^api/related$", "mpr.apiv1.related_products", name="api_related_products"),
    url(r"^api/detail$", "mpr.apiv1.product_detail", name="api_product_detail"),
    url(r"^api/search/by_product$", "mpr.apiv1.search_by_product", name="api_search_by_product"),
    url(r"^api/search/by_ingredient$", "mpr.apiv1.search_by_ingredient", name="api_search_by_ingredient"),
    url(r"^api/search$", "mpr.apiv1.search", name="api_search"),
    url(r"^api/search-lite$", "mpr.apiv1.search_lite", name="api_search_lite"),
    url(r"^api/dump$", "mpr.apiv1.dump", name="api_dump"),
    url(r"^api/v1/related$", "mpr.apiv1.related_products", name="api_related_products"),
    url(r"^api/v1/detail$", "mpr.apiv1.product_detail", name="api_product_detail"),
    url(r"^api/v1/search/by_product$", "mpr.apiv1.search_by_product", name="api_search_by_product"),
    url(r"^api/v1/search/by_ingredient$", "mpr.apiv1.search_by_ingredient", name="api_search_by_ingredient"),
    url(r"^api/v1/search$", "mpr.apiv1.search", name="api_search"),
    url(r"^api/v1/search-lite$", "mpr.apiv1.search_lite", name="api_search_lite"),
    url(r"^api/v1/dump$", "mpr.views.apiv1", name="api_dump"),
    url(r"^admin/", include(admin.site.urls)),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
