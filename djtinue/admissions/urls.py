from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djtinue.admissions.views',
    url(
        r'^inforequest/$','info_request',
        name='djtinue_inforequest'
    ),
    url(
        r'^inforequest/success/$',
        TemplateView.as_view(
            template_name='admissions/inforequest_success.html'
        ),
        name='djtinue_inforequest_success'
    ),
)
