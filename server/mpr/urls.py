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
            last_updated = LastUpdated.objects.all().reverse()[0]
            context['last_updated'] = last_updated
        except:
            context['last_updated'] = u"Never"
        return context

urlpatterns = patterns("",
    url(r'^$', IndexView.as_view(template_name="index.html"), name="home"),
    url(r"^api/related$", "mpr.views.related_products", name="api_related_products"),
    url(r"^api/detail$", "mpr.views.product_detail", name="api_product_detail"),
    url(r"^api/search/by_product$", "mpr.views.search_by_product", name="api_search_by_product"),
    url(r"^api/search/by_ingredient$", "mpr.views.search_by_ingredient", name="api_search_by_ingredient"),
    url(r"^api/search$", "mpr.views.search", name="api_search"),
    url(r"^api/search-lite$", "mpr.views.search_lite", name="api_search_lite"),
    url(r"^admin/", include(admin.site.urls)),
)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
