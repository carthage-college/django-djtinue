# -*- coding: utf-8 -*-

import requests
from django.conf import settings
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from djtools.utils.mail import send_mail
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from djtinue.admissions.forms import SESSION_TYPES
from djtinue.admissions.forms import InfoRequestForm
from djtinue.admissions.forms import InfoSessionForm


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def info_request(request):
    """Information request form."""
    if request.method == 'POST':
        form = InfoRequestForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # create out recipient list
            to = []
            # cleaned_data converts the data to a list so we do not
            # need to use getlist()
            for program in cd.get('academic_programs'):
                to = to + settings.CONTINUING_STUDIES_INFOREQUEST_RECIPIENTS[program]
            if settings.DEBUG:
                cd['to'] = to
                to = [settings.MANAGERS[0][1]]
            subject = 'OCS Information Request'
            send_mail(
                request,
                to,
                subject,
                cd['email'],
                'admissions/inforequest.txt',
                cd,
            )
            return HttpResponseRedirect(reverse_lazy('info_request_success'))
    else:
        form = InfoRequestForm()
    return render(request, 'admissions/inforequest.html', {'form': form})


def info_session(request, slug):
    """Information session request form."""
    if not SESSION_TYPES.get(slug):
        raise Http404
    if request.method == 'POST':
        form = InfoSessionForm(slug, request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            session_type = SESSION_TYPES[slug]
            cd['session_type'] = session_type
            # fetch event
            earl = '{0}/{1}/{2}@JSON'.format(
                settings.LIVEWHALE_API_URL,
                settings.LIVEWHALE_API_EVENTS_ID,
                cd['event'],
            )
            response = requests.get(earl)
            jason = response.json()
            cd['event'] = jason
            # to
            recipients = settings.CONTINUING_EDUCATION_INFOSESSION_RECIPIENTS[slug]
            subject = 'Master of Business Information Session Request: {0}'.format(
                session_type,
            )
            subject += '{0} on {1} ({2})'.format(
                session_type, jason['date'], jason['date_time'],
            )
            send_mail(
                request,
                recipients,
                subject,
                cd['email'],
                'admissions/infosession_email.html',
                cd,
            )
            return HttpResponseRedirect(reverse_lazy('info_session_success'))
    else:
        form = InfoSessionForm(slug)
    return render(request, 'admissions/infosession.html', {'form': form})
