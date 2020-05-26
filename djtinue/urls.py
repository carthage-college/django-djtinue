from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from django.contrib import admin

from djauth.views import loggedout


urlpatterns = [
    # django admin and loginas
    url('rocinante/', include('loginas.urls')),
    url('rocinante/', admin.site.urls),
    # admin honeypot
    url('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    # auth
    url(
        r'^accounts/login/$', auth_views.login,
        {'template_name': 'accounts/login.html'},
        name='auth_login'
    ),
    url(
        r'^accounts/logout/$', auth_views.logout,
        {'next_page': '/continuing-studies/forms/accounts/loggedout/'},
        name='auth_logout'
    ),
    url(
        r'^accounts/loggedout', loggedout,
        {'template_name': 'accounts/logged_out.html'}
    ),
    # apps
    url(
        r'^admissions/', include('djtinue.admissions.urls')
    ),
    url(
        r'^enrichment/', include('djtinue.enrichment.urls')
    ),
    # misc
    url(
        r'^denied/$',
        TemplateView.as_view(template_name='denied.html'), name='access_denied'
    ),
]
urlpatterns += url(r'^captcha/', include('captcha.urls')),
