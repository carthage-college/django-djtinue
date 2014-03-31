from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djtinue.admissions.application.views',
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name="admissions/application/done.html"
        ),
        name='admissions_application_success'
    ),
    url(
        r'^$',
        'admissions_application', name='admissions_application'
    ),
)
