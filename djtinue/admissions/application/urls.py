# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.urls import path
from djtinue.admissions.application import views


urlpatterns = [
    path('', views.form, name='admissions_application_default'),
    path(
        '<int:aid>/detail/',
        views.detail,
        name='admissions_application_detail',
    ),
    path(
        '<str:slug>/success/',
        views.success,
        name='admissions_application_success',
    ),
    path('<str:slug>/', views.form, name='admissions_application'),
]
