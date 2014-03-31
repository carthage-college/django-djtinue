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
    url(
       r'^information-session/success/$',
       TemplateView.as_view(
           template_name='admissions/infosession_success.html'
        ),
        name='info_session_success'
    ),
    url(
        r'^information-session/(?P<session_type>[a-zA-Z0-9_-]+)/$',
        'info_session', name="info_session"
    ),
    # application
    url(
        r'^application/',
        include('djtinue.admissions.application.urls')
    ),
)
