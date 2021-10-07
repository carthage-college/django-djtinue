# -*- coding: utf-8 -*-

import pytz
from django import forms
from django.db import connections
from django.utils.dateformat import DateFormat
from django.utils.encoding import force_text
from django.utils.timezone import localtime
from djforms.core.models import GenericChoice
from djtools.fields import STATE_CHOICES
from djtools.fields.localflavor import USPhoneNumberField
from localflavor.us.forms import USZipCodeField


TIME_OF_DAY = (
    ('Morning', 'Morning'),
    ('Afternoon', 'Afternoon'),
    ('Evening', 'Evening'),
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
)
# dictionary name corresponds to URL slug
SESSION_TYPES = {
    'information-session': 970,
    'graduate-education': 972,
    'undergraduate-studies': 973,
    'master-social-work': 980,
    'paralegal': 971,
    'business-design-innnovation': 1081,
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
        label='When would you like to be contacted?',
        choices=TIME_OF_DAY,
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
        cursor = connections['livewhale'].cursor()
        sql = """
            SELECT
                id, title, date_dt
            FROM
                livewhale_events
            WHERE
                id IN (
                    select id2 from livewhale_tags2any where id1={0}
                )
            AND
                id IN (
                    select id2 from livewhale_tags2any where id1={1}
                )
            AND
                date_dt > DATE(NOW())
            ORDER BY
                date_dt
        """.format(
            SESSION_TYPES['information-session'], SESSION_TYPES[session_type],
        )
        cursor.execute(sql)
        # Wed. May 01, 2020 at 06pm (Master of Education & ACT Info Session)
        choices = [('', '---choose a date---')]
        for event in cursor.fetchall():
            lc = localtime(pytz.utc.localize(event[2]))
            df = DateFormat(lc)
            day = df.format('D')
            date = df.format('M d, Y')
            time = df.format('h:ia')
            title = '{0}. {1} at {2} ({3})'.format(
                day, date, time, force_text(event[1]),
            )

            choices.append((event[0], title))
        self.fields['event'].choices = choices
