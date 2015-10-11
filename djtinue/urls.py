from django.conf.urls import patterns, include, url

from django.contrib import admin

#admin.autodiscover()

urlpatterns = patterns('',
    url(
        r'^admin/', include(admin.site.urls)
    ),
    url(
        r'^admissions/', include('djtinue.admissions.urls')
    ),
    #url(r'^bureau/', include('djtinue.bureau.urls')),
    url(
        r'^enrichment/', include('djtinue.enrichment.urls')
    ),
)
