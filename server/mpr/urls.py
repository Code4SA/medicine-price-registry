from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    url(r"^api/$", "mpr.views.api", name="api"),
    url(r"^admin/", include(admin.site.urls)),
)
