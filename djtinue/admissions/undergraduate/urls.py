from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djtinue.admissions.undergraduate.views',
    url(
        r'^application/success/$',
        TemplateView.as_view(
            template_name="admissions/undergraduate/done.html"
        ),
        name='undergraduate_admissions_success'
    ),
    url(
        r'^application/$',
        'admissions_application', name='undergraduate_admissions_application'
    ),
)
