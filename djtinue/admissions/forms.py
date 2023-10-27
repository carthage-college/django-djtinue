# -*- coding: utf-8 -*-

import requests
from django import forms
from django.conf import settings
from django.utils.encoding import force_str
from djforms.core.models import GenericChoice
from djtools.fields import STATE_CHOICES
from djtools.fields.localflavor import USPhoneNumberField
from localflavor.us.forms import USZipCodeField
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

CONTACT_HOW = (
    ('Email', 'Email'),
    ('Text', 'Text'),
    ('Phone', 'Phone'),
)
HEAR_ABOUT = (
    ('Education/Career Fair', 'Education/Career Fair'),
    ('Radio', 'Radio'),
    ('Newspaper', 'Newspaper'),
    ('Direct Mail', 'Direct Mail'),
    ('E-mail', 'E-mail'),
    ('Internet Search', 'Internet Search'),
    (
        'Information Session/Admissions Event',
        'Information Session/Admissions Event',
    ),
    ('Associate/Friend/Colleague', 'Associate/Friend/Colleague'),
    ('Referral-Advisor-Employer', 'Referral-Advisor-Employer'),
    ('I am a Carthage Graduate', 'I am a Carthage Graduate'),
    ('Carthage Website', 'Carthage Website'),
    ('Other', 'Other'),
)
ACADEMIC_PROGRAMS = (
    (
        "Undergraduate/Bachelor's Degree",
        "Undergraduate/Bachelor's Degree",
    ),
    (
        'Master of Science in Business: Design and Innovation Track',
        'Master of Science in Business: Design and Innovation Track',
    ),
    (
        'Master of Science in Business: Sports Management Track',
        'Master of Science in Business: Sports Management Track',
    ),
    (
        'Master of Music in Music Theatre Vocal Pedagogy',
        'Master of Music in Music Theatre Vocal Pedagogy',
    ),
    ('Master of Education', 'Master of Education'),
    ('Teacher Certification', 'Teacher Certification'),
    ('Athletic Training', 'Master of Athletic Training'),
)
# dictionary name corresponds to URL slug
SESSION_TYPES = {
    'information-session': 2071,
    'master-education': 2299,
    'business-design-innnovation': 2069,
    'business-sports-management': 2070,
}


def limit_format():
    """Format the generic choices for select field."""
    formats = [('', '----select----')]
    choices = GenericChoice.objects.filter(
        tags__name__in=['Admissions Contact Platform'],
    ).order_by('ranking')
    for choice in choices:
        formats.append((choice.name, choice.value))
    return formats


class InfoRequestForm(forms.Form):
    """Form class for the information request form."""

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = USPhoneNumberField(required=False, help_text='Format: XXX-XXX-XXXX')
    address = forms.CharField(required=False, label='Street Address')
    city = forms.CharField(required=False)
    state = forms.CharField(
        required=False,
        widget=forms.Select(choices=STATE_CHOICES),
    )
    postal_code = USZipCodeField(required=False, label='Zip Code')
    time_of_day = forms.MultipleChoiceField(
        label='How would you like to be contacted?',
        choices=CONTACT_HOW,
        widget=forms.CheckboxSelectMultiple(),
    )
    areas_study = forms.CharField(
        label='Intended Areas of Major/Study',
        widget=forms.Textarea,
    )
    academic_programs = forms.MultipleChoiceField(
        choices=ACADEMIC_PROGRAMS,
        widget=forms.CheckboxSelectMultiple(),
    )
    hear_about = forms.CharField(
        label='How did you hear about us?',
        widget=forms.Textarea,
    )


class InfoSessionForm(forms.Form):
    """Form class for the information session form."""

    event = forms.ChoiceField(choices=())
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    address = forms.CharField(label='Street Address')
    city = forms.CharField()
    state = forms.CharField(widget=forms.Select(choices=STATE_CHOICES))
    postal_code = USZipCodeField(label='Zip Code')
    phone = USPhoneNumberField(required=False, help_text='Format: XXX-XXX-XXXX')
    hear_about = forms.CharField(
        label='How did you hear about the program?',
        widget=forms.Textarea,
    )
    meeting_format = forms.CharField(
        widget=forms.Select(choices=limit_format()),
    )

    def __init__(self, session_type, *args, **kwargs):
        """Override the intitialization method to create date select field."""
        super(InfoSessionForm, self).__init__(*args, **kwargs)
        earl = '{0}/{1}/group/Admission%20&%20Aid/tag/information-session/tag/{2}'.format(
            settings.LIVEWHALE_API_URL,
            settings.LIVEWHALE_API_EVENTS,
            session_type,
        )
        response = requests.get(earl)
        jason = response.json()
        # Wed. May 01, 2020 at 06pm (Master of Education & ACT Info Session)
        choices = [('', '---choose a date---')]
        for jay in jason:
            title = '{0} at {1} ({2})'.format(
                jay['date'], jay['date_time'], force_str(jay['title']),
            )
            choices.append((jay['id'], title))
        self.fields['event'].choices = choices
