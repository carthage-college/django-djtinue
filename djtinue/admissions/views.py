from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext, loader, Context

from djtools.utils.mail import send_mail
from djtinue.admissions.forms import InfoRequestForm

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
                    if program in LOYOLA and 'mwest@carthage.edu' not in to:
                        to.append('mwest@carthage.edu')
                        to.append('jweiser@carthage.edu')
                    if program in CEDU1 and 'jweiser@carthage.edu' not in to:
                        to.append('jweiser@carthage.edu')
                    if program in CEDU1 and 'taugustine@carthage.edu' not in to:
                        to.append('taugustine@carthage.edu')
                    if program in CEDU2 and 'ldahl@carthage.edu' not in to:
                        to.append('ldahl@carthage.edu')
            if to == []:
                to.append('mwest@carthage.edu')
            if settings.DEBUG:
                to = TO
            to.append(cd['email'])
            subject = "Adult Education Information Request"
            send_mail(
                request, to, subject, cd["email"],
                "admissions/inforequest.txt", cd, BCC, content="text"
            )
            return HttpResponseRedirect(
                reverse_lazy("djtinue_inforequest_success")
            )
    else:
        form = InfoRequestForm()
    return render_to_response(
        'admissions/inforequest.html',{'form': form,},
        context_instance=RequestContext(request)
    )
