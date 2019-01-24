from django.conf import settings
from django.utils.dates import MONTHS
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404

from djtools.fields import STATE_CHOICES
from djtools.utils.mail import send_mail
from djforms.processors.models import Order
from djforms.processors.forms import TrustCommerceForm
from djtinue.admissions.application import _insert
from djtinue.admissions.application.forms import *
from djtinue.admissions.application.models import School

def admissions_application(request, stype):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL,]
    else:
        TO_LIST = ["jweiser@carthage.edu",]
    BCC = settings.MANAGERS

    schools = []
    order = None
    if request.method=='POST':
        try:
            education_goals_form = eval(stype.capitalize()+"Form")(request.POST)
        except:
            raise Http404

        contact_form = AdultContactForm(request.POST)
        personal_form = PersonalForm(request.POST)
        employment_form = EmploymentForm(request.POST)
        fee_form = ApplicationFeeForm(request.POST)
        # build the schools list
        x = 0
        while x < len(request.POST.getlist("school_name[]")):
            school = School(
                request.POST.getlist("school_code[]")[x],
                request.POST.getlist("school_name[]")[x],
                request.POST.getlist("school_city[]")[x],
                request.POST.getlist("school_state[]")[x],
                request.POST.getlist("from_month[]")[x],
                request.POST.getlist("from_year[]")[x],
                request.POST.getlist("to_month[]")[x],
                request.POST.getlist("to_year[]")[x],
                request.POST.getlist("grad_month[]")[x],
                request.POST.getlist("grad_year[]")[x]
            )
            schools.append(school)
            x += 1
        # delete the 'doop' element used for javascript clone
        del schools[0]

        if contact_form.is_valid() and \
          personal_form.is_valid() and \
          employment_form.is_valid() and \
          education_goals_form.is_valid() and fee_form.is_valid():
            contact = contact_form.cleaned_data
            personal = personal_form.cleaned_data
            employment = employment_form.cleaned_data
            education = education_goals_form.cleaned_data
            fee = fee_form.cleaned_data
            data = {
                'contact':contact,'personal':personal,
                'employment':employment,'education':education,
                'schools':schools,'fee':fee
            }
            total = fee['amount']
            # fetch the real name for educational goal,
            # so we can display it in email rather than ID
            goal = EDUCATION_GOAL[int(data['education']['educationalgoal'])-1][1]
            data['education']['educationalgoalname'] = goal
            subject = "[Undergraduate Admissions Application] %s, %s" % (
                contact['last_name'],contact['first_name']
            )
            email = contact['email']
            # credit card payment
            if fee['payment_type'] == "Credit Card":
                contact, created = Contact.objects.get_or_create(
                    first_name=contact['first_name'],
                    last_name=contact['last_name'],
                    second_name=contact['second_name'],
                    previous_name=contact['previous_name'],
                    email=email,phone=contact['phone'],
                    address1=contact['address1'],
                    address2=contact['address2'],city=contact['city'],
                    state=contact['state'],
                    postal_code=contact['postal_code']
                )
                order = Order(
                    total=total,auth="sale",status="In Process",
                    operator="DJTinueUgradAdmish"
                )
                payment_form = TrustCommerceForm(order, contact, request.POST)
                if payment_form.is_valid():
                    r = payment_form.processor_response
                    order.status = r.msg['status']
                    order.transid = r.msg['transid']
                    order.cc_name = payment_form.name
                    order.cc_4_digits = payment_form.card[-4:]
                    order.save()
                    contact.order.add(order)
                    data['order'] = order
                    # insert into informix and send mail
                    result = _insert(data)
                    # TODO: send email if result = fail, log data
                    send_mail(
                        request, TO_LIST, subject, contact.email,
                        "admissions/application/email.html", data, BCC
                    )
                    return HttpResponseRedirect(
                        reverse('admissions_application_success')
                    )
                else:
                    r = payment_form.processor_response
                    status = r.status
                    if r:
                        order.status = status
                    else:
                        order.status = "Blocked"
                    order.save()
                    contact.order.add(order)
            else:
                # insert and send mail
                result = _insert(data)
                # TODO: send email if result = fail, log data
                send_mail(
                    request, TO_LIST, subject,contact["email"],
                    "admissions/application/email.html", data, BCC
                )
                return HttpResponseRedirect(
                    reverse('admissions_application_success')
                )
        else:
            if request.POST.get('payment_type') == "Credit Card":
                payment_form = TrustCommerceForm(None, request.POST)
                payment_form.is_valid()
            else:
                payment_form = TrustCommerceForm()
    else:
        try:
            education_goals_form = eval(stype.capitalize()+"Form")()
        except:
            raise Http404
        contact_form = AdultContactForm()
        personal_form = PersonalForm()
        employment_form = EmploymentForm()
        fee_form = ApplicationFeeForm()
        payment_form = TrustCommerceForm()

    extra_context = {
        "contact_form":contact_form,"personal_form":personal_form,
        "order":order,"doop":len(schools),"states":STATE_CHOICES,
        "employment_form":employment_form,
        "education_goals_form":education_goals_form,
        "schools":schools,"fee_form":fee_form,"payment_form":payment_form,
        "months":MONTHS, "years1":YEARS1,"years3":YEARS3,"stype":stype
    }
    return render(
        request, 'admissions/application/form.html', extra_context
    )
