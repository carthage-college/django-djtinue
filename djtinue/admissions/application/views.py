# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from djforms.processors.forms import TrustCommerceForm
from djtools.utils.mail import send_mail

from djtinue.admissions.application.forms import ENTRY_YEAR_CHOICES
from djtinue.admissions.application.forms import ApplicationForm
from djtinue.admissions.application.forms import ContactForm
from djtinue.admissions.application.forms import EducationForm
from djtinue.admissions.application.forms import EducationRequiredForm
from djtinue.admissions.application.forms import OrderForm
from djtinue.admissions.application.models import Application


REQ = False
PROGRAM = {
    'bdi': 'Master (MSc) in Business Design & Innovation Application',
    'bsm': 'Master (MSc) in Business Sports Management Application',
    'bsn': 'RSN to BSN',
    'music': 'M.M. in Music Theatre Vocal Pedagogy',
}
SUBJECT = 'Application for Carthage'
EMAIL = 'Carthage Admissions <{email}>'.format


def form(request, slug=None):
    """Application form."""
    to_list = settings.ADMISSIONS_EMAILS.get(slug)
    path = prefix = 'admissions/application/'
    if to_list:
        path = os.path.join(prefix, slug)
    else:
        to_list = settings.ADMISSIONS_EMAILS['default']
    if settings.DEBUG:
        to_list = [settings.SERVER_MAIL]
    form_template = '{0}/form.html'.format(path)
    email_template = '{0}/email.html'.format(path)
    # recommendations are not required for some applications
    form_ct1 = None
    form_ct2 = None
    if request.method == 'POST':
        form_app = ApplicationForm(
            request.POST,
            request.FILES,
            label_suffix='',
            use_required_attribute=REQ,
        )
        if slug == 'music':
            form_ct1 = ContactForm(
                request.POST,
                prefix='ct1',
                label_suffix='',
                use_required_attribute=REQ,
            )
            form_ct2 = ContactForm(
                request.POST,
                prefix='ct2',
                label_suffix='',
                use_required_attribute=REQ,
            )
        form_ed1 = EducationRequiredForm(
            request.POST,
            request.FILES,
            prefix='ed1',
            label_suffix='',
            use_required_attribute=REQ,
        )
        form_ed2 = EducationForm(
            request.POST,
            request.FILES,
            prefix='ed2',
            label_suffix='',
            use_required_attribute=REQ,
        )
        form_ed3 = EducationForm(
            request.POST,
            request.FILES,
            prefix='ed3',
            label_suffix='',
            use_required_attribute=REQ,
        )
        form_ed4 = EducationForm(
            request.POST,
            request.FILES,
            prefix='ed4',
            label_suffix='',
            use_required_attribute=REQ,
        )
        form_ed5 = EducationForm(
            request.POST,
            request.FILES,
            prefix='ed5',
            label_suffix='',
            use_required_attribute=REQ,
        )
        form_ord = OrderForm(
            request.POST,
            label_suffix='',
            use_required_attribute=REQ,
            initial={'total': 35, 'avs': False, 'auth': 'sale'},
        )
        form_proc = TrustCommerceForm(
            request.POST,
            label_suffix='',
            use_required_attribute=False,
        )
        contacts = True
        if form_ct1 and form_ct2:
            contacts = (
                form_ct1.is_valid() and form_ct2.is_valid()
            )
        if form_app.is_valid() and form_ed1.is_valid() and form_ord.is_valid() and contacts:
            app = form_app.save()
            app.slug = slug
            app.social_security_four = app.social_security_number[-4:]
            app.save()
            # recommendations
            if slug == 'music':
                if form_ct1.is_valid():
                    ct1 = form_ct1.save(commit=False)
                    ct1.application = app
                    ct1.save()
                if form_ct2.is_valid():
                    ct2 = form_ct2.save(commit=False)
                    ct2.application = app
                    ct2.save()
            # schools
            ed1 = form_ed1.save(commit=False)
            ed1.application = app
            ed1.save()
            ed2 = form_ed2.save(commit=False)
            ed2.application = app
            ed2.save()
            ed3 = form_ed3.save(commit=False)
            ed3.application = app
            ed3.save()
            ed4 = form_ed4.save(commit=False)
            ed4.application = app
            ed4.save()
            ed5 = form_ed5.save(commit=False)
            ed5.application = app
            ed5.save()
            # transaction
            order = form_ord.save()
            order.total = 35.00
            order.operator = settings.TC_OPERATOR
            program = ''
            if slug:
                program = PROGRAM[slug]
            subject = '{0} {1}: ({2}, {3})'.format(
                SUBJECT, program, app.last_name, app.first_name,
            )
            if app.payment_method == 'Credit Card':

                form_proc = TrustCommerceForm(
                    order, app, request.POST, use_required_attribute=False,
                )

                if form_proc.is_valid():
                    response = form_proc.processor_response
                    order.status = response.msg['status']
                    order.transid = response.msg['transid']
                    order.cc_name = form_proc.name
                    order.cc_four_digits = form_proc.card[-4:]
                    order.save()
                    app.order.add(order)
                    order.app = app
                    sent = send_mail(
                        request,
                        to_list,
                        subject,
                        EMAIL(email=app.email),
                        email_template,
                        order,
                    )
                    order.send_mail = sent
                    order.save()

                    return HttpResponseRedirect(
                        reverse(
                            'admissions_application_success',
                            kwargs={'slug': slug},
                        ),
                    )

                else:
                    response = form_proc.processor_response
                    if response:
                        order.status = response.status
                    else:
                        order.status = 'Form Invalid'
                    order.cc_name = form_proc.name
                    if form_proc.card:
                        order.cc_four_digits = form_proc.card[-4:]
                    order.save()
                    app.order.add(order)
            else:
                order.auth = 'COD'
                order.status = 'Pay later'
                order.save()
                app.order.add(order)
                # used for email rendering
                order.app = app
                sent = send_mail(
                    request,
                    to_list,
                    subject,
                    EMAIL(email=app.email),
                    email_template,
                    order,
                )
                order.send_mail = sent
                order.save()
                return HttpResponseRedirect(
                    reverse(
                        'admissions_application_success',
                        kwargs={'slug': slug},
                    ),
                )
        else:
            if request.POST.get('payment_method') == 'Credit Card':
                form_proc = TrustCommerceForm(
                    None, request.POST, use_required_attribute=False,
                )
                form_proc.is_valid()
            else:
                form_proc = TrustCommerceForm(use_required_attribute=False)
    else:
        form_app = ApplicationForm(
            label_suffix='', use_required_attribute=REQ,
        )
        if slug == 'music':
            form_ct1 = ContactForm(
                prefix='ct1', label_suffix='', use_required_attribute=REQ,
            )
            form_ct2 = ContactForm(
                prefix='ct2', label_suffix='', use_required_attribute=REQ,
            )
        form_ed1 = EducationRequiredForm(
            prefix='ed1', label_suffix='', use_required_attribute=REQ,
        )
        form_ed2 = EducationForm(
            prefix='ed2', label_suffix='', use_required_attribute=REQ,
        )
        form_ed3 = EducationForm(
            prefix='ed3', label_suffix='', use_required_attribute=REQ,
        )
        form_ed4 = EducationForm(
            prefix='ed4', label_suffix='', use_required_attribute=REQ,
        )
        form_ed5 = EducationForm(
            prefix='ed5', label_suffix='', use_required_attribute=REQ,
        )
        form_ord = OrderForm(
            label_suffix='',
            use_required_attribute=REQ,
            initial={'total': 35, 'avs': False, 'auth': 'sale'},
        )
        form_proc = TrustCommerceForm(
            label_suffix='', use_required_attribute=False,
        )

    extra_context = {
        'form_app': form_app,
        'form_ct1': form_ct1,
        'form_ct2': form_ct2,
        'form_ord': form_ord,
        'form_ed1': form_ed1,
        'form_ed2': form_ed2,
        'form_ed3': form_ed3,
        'form_ed4': form_ed4,
        'form_ed5': form_ed5,
        'form_proc': form_proc,
        'slug': slug,
        'years': ENTRY_YEAR_CHOICES,
        'terms': ENTRY_YEAR_CHOICES,
    }

    return render(request, form_template, extra_context)


@login_required
def detail(request, aid):
    """Display the details of an application."""
    application = get_object_or_404(Application, pk=aid)
    return render(
        request,
        'admissions/application/email.html',
        {'data': {'app': application}},
    )


def success(request, slug):
    """Redirect here after user submits application form."""
    template = 'admissions/application/done.html'
    return render(request, template, {'slug': slug})
