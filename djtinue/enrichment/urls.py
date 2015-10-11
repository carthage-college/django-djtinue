from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djtinue.enrichment.views',
    # registration
    url(
        r'^registration/success/$',
        TemplateView.as_view(
            template_name="enrichment/registration_done.html"
        ),
        name="enrichment_registration_success"
    ),
    url(
        r'^registration/$', 'index',
        name="enrichment_registration"
    ),
)
