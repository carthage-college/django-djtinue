from django.urls import path, re_path
from django.views.generic import TemplateView

from djtinue.admissions.application import views


urlpatterns = [
    path(
        '',
        views.form, name='admissions_application_default'
    ),
    path(
        'success/',
        TemplateView.as_view(
            template_name='admissions/application/done.html'
        ),
        name='admissions_application_success'
    ),
    re_path(
        r'^(?P<aid>\d+)/detail/$',
        views.detail, name='admissions_application_detail'
    ),
    re_path(
        r'^(?P<slug>[a-zA-Z0-9_-]+)/$',
        views.form, name='admissions_application'
    )
]
