from django.conf.urls import url
from django.views.generic import TemplateView

form djtinue.admissions.application import views

urlpatterns = [
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='admissions/application/done.html'
        ),
        name='admissions_application_success'
    ),
    url(
        r'^(?P<stype>[a-zA-Z0-9_-]+)/$',
        views.admissions_application, name='admissions_application'
    ),
]
