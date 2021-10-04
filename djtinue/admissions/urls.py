from django.urls import include, path, re_path
from django.views.generic import TemplateView

from djtinue.admissions import views


urlpatterns = [
    # information request
    path(
        'information-request/', views.info_request, name='info_request'
    ),
    path(
        'information-request/success/',
        TemplateView.as_view(
            template_name='admissions/inforequest_success.html'
        ),
        name='info_request_success'
    ),
    path(
       'information-session/success/',
       TemplateView.as_view(
           template_name='admissions/infosession_success.html'
        ),
        name='info_session_success'
    ),
    re_path(
        r'^information-session/(?P<session_type>[a-zA-Z0-9_-]+)/$',
        views.info_session, name='info_session'
    ),
    # application
    path(
        'application/', include('djtinue.admissions.application.urls')
    ),
]
