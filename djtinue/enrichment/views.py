from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from djtinue.enrichment.models import Course, Registration
from djtinue.enrichment.forms import RegistrationForm, RegistrationOrderForm

from djforms.processors.models import Contact, Order
from djforms.processors.forms import TrustCommerceForm

from djtools.utils.mail import send_mail

REQ = True
if settings.DEBUG:
    REQ = False


def index(request):
    status = None
    msg = None
    discount = "No"
    # fetch active courses
    courses = Course.objects.filter(active=True)
    if request.POST:
        form_reg = RegistrationForm(
            request.POST, label_suffix='', use_required_attribute=REQ
        )
        form_ord = RegistrationOrderForm(
            request.POST, label_suffix='', use_required_attribute=REQ
        )
        # process the courses selected and compare to courses active
        selected_courses = request.POST.getlist("courses[]")
        for c in courses:
            c.checked = False
            if str(c.id) in selected_courses:
                c.checked = True
        if form_reg.is_valid() and form_ord.is_valid():
            BCC = settings.MANAGERS
            if settings.DEBUG:
                TO_LIST = [settings.ADMINS[0][1],]
            else:
                TO_LIST = [
                    settings.CONTINUING_STUDIES_ENRICHMENT_REGISTRATION_EMAIL,
                ]
            contact = form_reg.save()
            contact.social_security_four = contact.social_security_number[-4:]
            contact.save()
            discount = contact.attended_before
            data_ord = form_ord.cleaned_data
            order = Order(
                total=data_ord["total"],auth="sale",status="In Process",
                operator="DJTinueEnrichmentReg"
            )
            form_proc = TrustCommerceForm(
                order, contact, request.POST, use_required_attribute=REQ
            )
            # add courses to contact object's m2m relationship
            for c in courses:
                if c.checked:
                    contact.courses.add(c)
            # off to trust commerce for cc auth
            if form_proc.is_valid():
                r = form_proc.processor_response
                order.status = r.msg['status']
                order.transid = r.msg['transid']
                order.cc_name = form_proc.name
                order.cc_4_digits = form_proc.card[-4:]
                order.save()
                contact.order.add(order)
                order.reg = contact
                email = None
                if contact.email:
                    email = contact.email
                elif contact.email_work:
                    email = contact.email_work
                TO_LIST.append(email)
                sent = send_mail(
                    request, TO_LIST,
                    "Enrichment registration",
                    email,
                    "enrichment/registration_email.html",
                    order, BCC
                )
                order.send_mail = sent
                order.save()
                return HttpResponseRedirect(
                    reverse('enrichment_registration_success')
                )
            else:
                r = form_proc.processor_response
                if r:
                    order.status = r.status
                else:
                    order.status = "Validation error"
                order.cc_name = form_proc.name
                if form_proc.card:
                    order.cc_4_digits = form_proc.card[-4:]
                order.save()
                contact.order.add(order)
                status = order.status
                order.reg = contact
        else:
            form_proc = TrustCommerceForm(
                None, request.POST, use_required_attribute=REQ
            )
            form_proc.is_valid()
            discount = form_reg.cleaned_data.get("attended_before")
    else:
        initial = {'avs':False,'auth':'sale'}
        form_reg = RegistrationForm(
            label_suffix='', use_required_attribute=REQ
        )
        form_ord = RegistrationOrderForm(
            initial=initial, label_suffix='', use_required_attribute=REQ
        )
        form_proc = TrustCommerceForm(use_required_attribute=REQ)
    return render(
        request, 'enrichment/registration_form.html', {
            'form_reg': form_reg,'form_proc':form_proc,'form_ord': form_ord,
            'status':status,'msg':msg,'discount':discount,'courses':courses
        }
    )


@staff_member_required
def registration_print(request, rid):

    data = get_object_or_404(Registration, pk=rid)
    data.trans = data.order.first()

    return render(
        request,
        "enrichment/registration_print.html",
        {'data': data,},
    )
