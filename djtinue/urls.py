from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin

#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admissions/', include('djtinue.admissions.urls')),
    url(r'^graduate/', include('djtinue.graduate.urls')),
    url(r'^undergraduate/', include('djtinue.undergraduate.urls')),
)
