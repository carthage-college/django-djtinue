from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from djtinue.enrichment import BCC, TO_LIST
from djtinue.enrichment.forms import RegistrationForm, RegistrationOrderForm

from djforms.processors.models import Contact, Order
from djforms.processors.forms import TrustCommerceForm

from djtools.utils.mail import send_mail

def index(request):
    status = None
    msg = None
    if request.POST:
        form_reg = RegistrationForm(request.POST)
        form_ord = RegistrationOrderForm(request.POST)
        if form_reg.is_valid() and form_ord.is_valid():
            contact = form_reg.save()
            data_ord = form_ord.cleaned_data
            order = Order(
                total=data_ord["total"],auth="sale",status="In Process",
                operator="DJTinueEnrichmentReg"
            )
            form_proc = TrustCommerceForm(order, contact, request.POST)
            if form_proc.is_valid():
                r = form_proc.processor_response
                order.status = r.msg['status']
                order.transid = r.msg['transid']
                order.cc_name = form_proc.name
                order.cc_4_digits = form_proc.card[-4:]
                order.save()
                contact.order.add(order)
                order.reg = contact
                send_mail(
                    request, TO_LIST,
                    "Enrichment registration",
                    contact.email,
                    "enrichment/registration_email.html",
                    order, BCC
                )
                return HttpResponseRedirect(
                    reverse('enrichment_registration_success')
                )
            else:
                r = form_proc.processor_response
                if r:
                    order.status = r.status
                else:
                    order.status = "Blocked"
                order.cc_name = form_proc.name
                if form_proc.card:
                    order.cc_4_digits = form_proc.card[-4:]
                order.save()
                contact.order.add(order)
                status = order.status
                order.reg = contact
                send_mail(
                    request, TO_LIST,
                    "[{}] Enrichment registration".format(status),
                    contact.email,
                    "enrichment/registration_email.html",
                    order, BCC
                )
        else:
            form_proc = TrustCommerceForm(None, request.POST)
            form_proc.is_valid()
    else:
        initial = {'avs':False,'auth':'sale'}
        form_reg = RegistrationForm()
        form_ord = RegistrationOrderForm(initial=initial)
        form_proc = TrustCommerceForm()
    return render_to_response(
        'enrichment/registration_form.html',
        {
            'form_reg': form_reg,'form_proc':form_proc,'form_ord': form_ord,
            'status':status,'msg':msg,
        }, context_instance=RequestContext(request)
    )
