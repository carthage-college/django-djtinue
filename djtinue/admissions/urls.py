from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djtinue.admissions.views',
    url(
        r'^inforequest/$','info_request',
        name='continuing_education_info_request'
    ),
    url(
        r'^inforequest/success/$',
        TemplateView.as_view(
            template_name='continuing-education/inforequest_success.html'
        )
    ),
)
