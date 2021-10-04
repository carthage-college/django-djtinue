# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.urls import include
from django.urls import path
from django.views.generic import TemplateView
from djtinue.admissions import views


urlpatterns = [
    path(
        'information-request/', views.info_request, name='info_request',
    ),
    path(
        'information-request/success/',
        TemplateView.as_view(
            template_name='admissions/inforequest_success.html',
        ),
        name='info_request_success',
    ),
    path(
        'information-session/success/',
        TemplateView.as_view(
            template_name='admissions/infosession_success.html',
        ),
        name='info_session_success',
    ),
    path(
        'information-session/<str:session_type>/',
        views.info_session,
        name='info_session',
    ),
    path(
        'application/', include('djtinue.admissions.application.urls'),
    ),
]
