from django import forms
from localflavor.us.forms import USPhoneNumberField, USZipCodeField
from djtools.fields import STATE_CHOICES

TIME_OF_DAY =  [
    ('Morning', 'Morning'),
    ('Afternoon', 'Afternoon'),
    ('Evening', 'Evening'),
]
HEAR_ABOUT =  [
    ('Education/Career Fair', 'Education/Career Fair'),
    ('Radio', 'Radio'),
    ('Newspaper', 'Newspaper'),
    ('Direct Mail', 'Direct Mail'),
    ('E-mail', 'E-mail'),
    ('Internet Search', 'Internet Search'),
    (
        'Information Session/Admissions Event',
        'Information Session/Admissions Event'
    ),
    ('Associate/Friend/Colleague', 'Associate/Friend/Colleague'),
    ('Referral-Advisor-Employer', 'Referral-Advisor-Employer'),
    ('I am a Carthage Graduate', 'I am a Carthage Graduate'),
    ('Carthage Website', 'Carthage Website'),
    ('Other', 'Other'),
]
ACADEMIC_PROGRAMS =  [
    ('Semester Programs', 'Semester Programs'),
    ('Accelerated Programs', 'Accelerated Programs'),
    ('Master of Education', 'Master of Education'),
    ('Loyola Master of Social Work', 'Loyola Master of Social Work'),
    (
        'Accelerated Certification for Teachers',
        'Accelerated Certification for Teachers'
    ),
    ('Paralegal Program', 'Paralegal Program'),
    (
        'Enrichment and Continuing Education',
        'Enrichment and Continuing Education'
    ),
    ('Summer Language Seminars', 'Summer Language Seminars'),
]

class InfoRequestForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = USPhoneNumberField(required=False,help_text="Format: XXX-XXX-XXXX")
    address = forms.CharField(required=False,label="Street Address")
    city = forms.CharField(required=False)
    state = forms.CharField(
        required=False,
        widget=forms.Select(choices=STATE_CHOICES)
    )
    postal_code = USZipCodeField(required=False,label="Zip Code")
    time_of_day = forms.TypedChoiceField(
        label="When would you like to be contacted?",
        choices=TIME_OF_DAY, widget=forms.RadioSelect()
    )
    academic_programs = forms.MultipleChoiceField(
        choices=ACADEMIC_PROGRAMS,
        widget=forms.CheckboxSelectMultiple()
    )
    hear_about = forms.TypedChoiceField(
        label="How did you hear about us?",
        choices=HEAR_ABOUT, widget=forms.RadioSelect()
    )
    hear_other = forms.CharField(
        label="If other, please specify",
        required=False, widget=forms.Textarea
    )
