from django.conf.urls import url
from django.views.generic import TemplateView

from djtinue.enrichment import views

urlpatterns = [
    # registration
    url(
        r'^registration/success/$',
        TemplateView.as_view(
            template_name='enrichment/registration_done.html'
        ),
        name='enrichment_registration_success'
    ),
    url(
        r'^registration/(?P<rid>\d+)/print/$',
        views.registration_print, name='registration_print'
    ),
    url(
        r'^registration/$', views.index,
        name='enrichment_registration'
    ),
]
