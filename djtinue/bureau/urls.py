from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('djtinue.graduate',
    url(
        r'^candidacy/success/$',
        TemplateView.as_view(template_name="graduate/candidacy/done.html"),
        name='graduate_candidacy_success'
    ),
    url(
        r'^candidacy/$',
        'candidacy.views.index', name='index'
    ),
)
