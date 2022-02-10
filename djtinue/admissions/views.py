# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
#from django.utils.dateformat import DateFormat
#from django.utils.timezone import localtime
from djtinue.admissions.forms import SESSION_TYPES
from djtinue.admissions.forms import InfoRequestForm
from djtinue.admissions.forms import InfoSessionForm
#from djtinue.admissions.models import LivewhaleEvents as Event
from djtools.utils.mail import send_mail


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


def info_session(request, session_type):
    """Information session request form."""
    try:
        SESSION_TYPES[session_type]
    except Exception:
        raise Http404
    if request.method == 'POST':
        form = InfoSessionForm(session_type, request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['session_type'] = session_type
            # fetch event
            #event = Event.objects.using('livewhale').get(pk=cd['event'])
            #cd['event'] = event
            # munge datetime
            #lc = localtime(event.date_dt)
            #df = DateFormat(lc)
            #day = df.format('D')
            #date = df.format('M d, Y')
            #time = df.format('h:ia')
            #datetime = '%s. %s at %s' % (day, date, time)
            #cd['datetime'] = datetime
            # to
            recipients = settings.CONTINUING_EDUCATION_INFOSESSION_RECIPIENTS
            to = recipients[session_type]
            #subject = 'OCS Information Session Request: '
            subject = 'OCS Information Session Request: {0}'.format(session_type)
            #subject += '{0} on {1}'.format(session_type, datetime)
            send_mail(
                request,
                to,
                subject,
                cd['email'],
                'admissions/infosession.txt',
                cd,
                content='',
            )
            return HttpResponseRedirect(reverse_lazy('info_session_success'))
    else:
        form = InfoSessionForm(session_type)
    return render(request, 'admissions/infosession.html', {'form': form})
