from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('djtinue.admissions.views',
    # information request
    url(
        r'^information-request/$','info_request',
        name='info_request'
    ),
    url(
        r'^information-request/success/$',
        TemplateView.as_view(
            template_name='admissions/inforequest_success.html'
        ),
        name='info_request_success'
    ),
    # undergraduate
    url(
        r'^undergraduate/',
        include('djtinue.admissions.undergraduate.urls')
    ),
    # graduate
    #url(
    #    r'^graduate/',
    #    include('djtinue.admissions.graduate.urls')
    #),
)
