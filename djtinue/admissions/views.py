from django.conf import settings
from django.template import RequestContext
from django.utils.timezone import localtime
from django.utils.dateformat import DateFormat
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, Http404

from djtinue.admissions.forms import InfoRequestForm, STYPES
from djtinue.admissions.forms import InfoSessionForm
from djtinue.admissions.models import LivewhaleEvents as Event

from djtools.utils.mail import send_mail

BCC = settings.MANAGERS
TO = [settings.SERVER_MAIL]

LOYOLA = ["Loyola MBA for Executives","Loyola Master of Social Work"]
CEDU1 = [
    "Master of Education","Accelerated Certification for Teachers",
    "Summer Language Seminars","Semester Programs","Accelerated Programs",
    "Paralegal Program","A.O.D.A."
]
CEDU2 = [
    "Enrichment and Continuing Education","Master of Education",
    "Accelerated Certification for Teachers","Summer Language Seminars",
    "Semester Programs","Accelerated Programs","Paralegal Program","A.O.D.A."
]

def info_request(request):
    if request.method == 'POST':
        form = InfoRequestForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            to = []
            if request.POST.has_key('academic_programs'):
                academic_programs = request.POST.getlist('academic_programs')
                for program in list(academic_programs):
                    #if program in LOYOLA and 'mwest@carthage.edu' not in to:
                    if program in LOYOLA:
                        #to.append('mwest@carthage.edu')
                        to.append('jweiser@carthage.edu')
                    if program in CEDU1 and 'jweiser@carthage.edu' not in to:
                        to.append('jweiser@carthage.edu')
                    if program in CEDU1 and 'taugustine@carthage.edu' not in to:
                        to.append('taugustine@carthage.edu')
                    if program in CEDU2 and 'ldahl@carthage.edu' not in to:
                        to.append('ldahl@carthage.edu')
            if to == []:
                #to.append('mwest@carthage.edu')
                to.append('jweiser@carthage.edu')
            if settings.DEBUG:
                to = TO
            to.append(cd['email'])
            subject = "GPS Information Request"
            send_mail(
                request, to, subject, cd["email"],
                "admissions/inforequest.txt", cd, BCC, content=""
            )
            return HttpResponseRedirect(
                reverse_lazy("info_request_success")
            )
    else:
        form = InfoRequestForm()
    return render_to_response(
        'admissions/inforequest.html',{'form': form,},
        context_instance=RequestContext(request)
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
            cd["session_type"] = session_type
            # fetch event
            event = Event.objects.using('livewhale').get(pk=cd['event'])
            cd["event"] = event
            # munge datetime
            lc = localtime(event.date_dt)
            df = DateFormat(lc)
            day = df.format('D')
            date = df.format('M d, Y')
            time = df.format('h:ia')
            datetime = "%s. %s at %s" % (day, date, time)
            cd["datetime"] = datetime
            # to
            recipients = settings.CONTINUING_EDUCATION_INFOSESSION_RECIPIENTS
            to = recipients[session_type]
            if settings.DEBUG:
                to = TO
            subject = "GPS Information Session Request: "
            subject +="%s on %s" % (session_type, datetime)
            send_mail(
                request, to, subject, cd["email"],
                "admissions/infosession.txt", cd, BCC, content=""
            )
            return HttpResponseRedirect(
                reverse_lazy("info_session_success")
            )
    else:
        form = InfoSessionForm(session_type)
    return render_to_response(
        'admissions/infosession.html',{'form': form,},
        context_instance=RequestContext(request)
    )
