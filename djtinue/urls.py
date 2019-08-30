from django.conf.urls import include, url
from django.views.generic import TemplateView

from django.contrib import admin

#admin.autodiscover()


urlpatterns = [
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
    url(
        r'^denied/$',
        TemplateView.as_view(template_name='denied.html'), name='access_denied'
    ),
]
urlpatterns += url(r'^captcha/', include('captcha.urls')),
