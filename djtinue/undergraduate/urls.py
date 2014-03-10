from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('djtinue.undergraduate.admissions.views',
    url(
        r'^success/$',
        TemplateView.as_view(template_name="admissions/undergraduate/done.html"),
        name='undergraduate_admissions_success'
    ),
    url(
        r'^undergraduate/$',
        'undergraduate_admissions_form', name='undergraduate_admissions_form'
    ),
    url(
        r'^masters/$',
        'djtinue.graduate.views.index', name='index'
    ),
)
