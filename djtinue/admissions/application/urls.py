from django.conf.urls import url
from django.views.generic import TemplateView

from djtinue.admissions.application import views


urlpatterns = [
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='admissions/application/done.html'
        ),
        name='admissions_application_success'
    ),
    url(
        r'^$',
        views.form, name='admissions_application_default'
    ),
    url(
        r'^(?P<slug>[a-zA-Z0-9_-]+)/$',
        views.form, name='admissions_application'
    )
]
