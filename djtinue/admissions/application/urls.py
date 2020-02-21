from django.conf.urls import url as path
from django.views.generic import TemplateView

from djtinue.admissions.application import views


urlpatterns = [
    path(
        r'^$',
        views.form, name='admissions_application_default'
    ),
    path(
        #'<str:slug>/success/',
        r'^(?P<slug>[a-zA-Z0-9_-]+)/success/',
        views.success,
        name='admissions_application_success'
    ),
    path(
        r'^(?P<aid>\d+)/detail/$',
        views.detail, name='admissions_application_detail'
    ),
    path(
        r'^(?P<slug>[a-zA-Z0-9_-]+)/$',
        views.form, name='admissions_application'
    ),
]
