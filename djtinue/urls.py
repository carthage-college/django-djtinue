# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include
from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from djauth.views import loggedout


urlpatterns = [
    # django admin
    path('rocinante/', admin.site.urls),
    #path('admin/', admin.site.urls),
    path('rocinante/', include('loginas.urls')),
    #path('admin/', include('loginas.urls')),
    # auth
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(),
        {'template_name': 'registration/login.html'},
        name='auth_login',
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        {'next_page': reverse_lazy('auth_loggedout')},
        name='auth_logout',
    ),
    path(
        'accounts/loggedout/',
        loggedout,
        {'template_name': 'registration/logged_out.html'},
        name='auth_loggedout',
    ),
    path(
        'accounts/',
        RedirectView.as_view(url=reverse_lazy('auth_login')),
    ),
    path(
        'denied/',
        TemplateView.as_view(template_name='denied.html'),
        name='access_denied',
    ),
    path('admissions/', include('djtinue.admissions.urls')),
    path('captcha/', include('captcha.urls')),
]
