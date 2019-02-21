from django.conf import settings
from django.utils.timezone import localtime
from django.utils.dateformat import DateFormat
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, Http404

from djtinue.admissions.forms import InfoRequestForm, STYPES
from djtinue.admissions.forms import InfoSessionForm
from djtinue.admissions.models import LivewhaleEvents as Event

from djtools.utils.mail import send_mail

BCC = settings.MANAGERS
TO = [settings.SERVER_MAIL]

CEDU1 = [
    'Master of Education','Accelerated Certification for Teachers',
    'Summer Language Seminars','Part-Time Semester',
    '7-Week Adult Undergraduate',
    'Paralegal Program','A.O.D.A.',
    'Master of Science in Business, Design and Innovation'
]
CEDU2 = [
    'Enrichment','Master of Education',
    'Accelerated Certification for Teachers','Summer Language Seminars',
    'Part-Time Semester','Paralegal Program','A.O.D.A.',
    '7-Week Adult Undergraduate',
    'Master of Science in Business, Design and Innovation'
]


def info_request(request):
    if request.method == 'POST':
        form = InfoRequestForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            to = settings.INFORMATION_REQUEST_EMAIL_LIST
            if settings.DEBUG:
                to = TO
            to.append(cd['email'])
            subject = "OCS Information Request"
            send_mail(
                request, to, subject, cd['email'],
                'admissions/inforequest.txt', cd, BCC, content=''
            )
            return HttpResponseRedirect(
                reverse_lazy('info_request_success')
            )
    else:
        form = InfoRequestForm()
    return render(
        request, 'admissions/inforequest.html',{'form': form,}
    )


def info_session(request, session_type):
    try:
        STYPES[session_type]
    except:
        raise Http404, "Page not found"
    if request.method == 'POST':
        form = InfoSessionForm(session_type,request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['session_type'] = session_type
            # fetch event
            event = Event.objects.using('livewhale').get(pk=cd['event'])
            cd['event'] = event
            # munge datetime
            lc = localtime(event.date_dt)
            df = DateFormat(lc)
            day = df.format('D')
            date = df.format('M d, Y')
            time = df.format('h:ia')
            datetime = '%s. %s at %s' % (day, date, time)
            cd['datetime'] = datetime
            # to
            recipients = settings.CONTINUING_EDUCATION_INFOSESSION_RECIPIENTS
            to = recipients[session_type]
            if settings.DEBUG:
                to = TO
            subject = "OCS Information Session Request: "
            subject +="%s on %s" % (session_type, datetime)
            send_mail(
                request, to, subject, cd['email'],
                'admissions/infosession.txt', cd, BCC, content=''
            )
            return HttpResponseRedirect(
                reverse_lazy('info_session_success')
            )
    else:
        form = InfoSessionForm(session_type)
    return render(
        request, 'admissions/infosession.html',{'form': form,}
    )
