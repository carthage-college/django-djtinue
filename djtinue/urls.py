from django.urls import include, path
from django.views.generic import TemplateView

from django.contrib import admin


urlpatterns = [
    # django admin
    path('rocinante/', include('loginas.urls')),
    path('rocinante/', admin.site.urls),
    # admin honeypot
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    # auth
    path(
        'accounts/login/', auth_views.LoginView.as_view(),
        {'template_name': 'registration/login.html'},
        name='auth_login'
    ),
    path(
        'accounts/logout/', auth_views.LogoutView.as_view(),
        {'next_page': reverse_lazy('auth_loggedout')},
        name='auth_logout'
    ),
    path(
        'accounts/loggedout/', loggedout,
        {'template_name': 'registration/logged_out.html'},
        name='auth_loggedout'
    ),
    path(
        'accounts/',
        RedirectView.as_view(url=reverse_lazy('auth_login'))
    ),
    path(
        'denied/',
        TemplateView.as_view(template_name='denied.html'), name='access_denied'
    ),
    #
    path(
        'admissions/', include('djtinue.admissions.urls')
    ),
]
urlpatterns += path('captcha/', include('captcha.urls')),
