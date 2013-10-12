from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="home"),
    url(r"^api/$", "mpr.views.api", name="api"),
    url(r"^admin/", include(admin.site.urls)),
)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
