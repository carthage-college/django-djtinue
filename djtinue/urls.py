from django.conf.urls import include, url

from django.contrib import admin

#admin.autodiscover()

urlpatterns = [
    #url(
        #r'^grappelli/', include('grappelli.urls')
    #),
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
]
