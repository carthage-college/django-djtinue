from django import forms
from django.conf import settings

from djtinue.admissions.application.models import Application
from djtinue.admissions.application.models import Contact
from djtinue.admissions.application.models import PAYMENT_CHOICES
from djtinue.admissions.application.models import School

from djtools.fields import BINARY_CHOICES, GENDER_CHOICES, TODAY
from djforms.processors.models import Order
from djforms.core.models import GenericChoice, GenericContact
from djforms.processors.forms import OrderForm

RACES = GenericChoice.objects.filter(
    tags__name__in=['Race'],
).order_by('ranking')
FELLOWSHIPS = GenericChoice.objects.filter(
    tags__name__in=['Fellowships'],
).order_by('ranking')
DATES = GenericChoice.objects.filter(
    tags__name='Audition Date',
).order_by('ranking')
TIMES = GenericChoice.objects.filter(
    tags__name='Audition Time',
).order_by('ranking')

year = TODAY.year
if (TODAY.month > 9):
    year += 1

ENTRY_TERM_CHOICES = (
    (year, 'Fall {}'.format(year)),
    (year+1, 'Fall {}'.format(year+1))
)


class ApplicationForm(forms.ModelForm):
    """
    Continuing Studies admissions application form submission
    """

    previous_name = forms.CharField(
        label="Previous last name",
        max_length=128, required=False
    )
    address1 = forms.CharField(
        label="Address",
        max_length=255, required=True
    )
    address2 = forms.CharField(
        label="",
        max_length=255, required=False
    )
    city = forms.CharField(
        label="City",
        max_length=128, required=True
    )
    state = forms.CharField(
        label="State/Province",
        max_length=128, required=True
    )
    postal_code = forms.CharField(
        label="Postal code",
        max_length=10, required=True
    )
    phone = forms.CharField(
        label="Primary phone",
        max_length=16, required=True
    )
    phone_secondary = forms.CharField(
        label="Phone 2",
        max_length=16, required=False
    )
    phone_tertiary = forms.CharField(
        label="Phone 3",
        max_length=16, required=False
    )
    social_security_number = forms.CharField(
        label="Social Security or National Identity number",
        max_length=16, required=False
    )
    latinx = forms.TypedChoiceField(
        label="Are you Hispanic or Latino?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect(),
        required=False
    )
    race = forms.ModelMultipleChoiceField(
        queryset = RACES,
        help_text = 'Check all that apply',
        widget = forms.CheckboxSelectMultiple(),
        required=False
    )
    gender = forms.TypedChoiceField(
        choices = GENDER_CHOICES,
        widget = forms.RadioSelect()
    )
    tuition_reimbursement = forms.TypedChoiceField(
        label="Does your employer offer tuition reimbursement?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect(),
        required=False
    )
    military = forms.TypedChoiceField(
        label="Have you ever served in the military?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect()
    )
    entry_year = forms.TypedChoiceField(
        label="When do you plan to start your studies?",
        choices=ENTRY_TERM_CHOICES, widget=forms.RadioSelect()
    )
    fellowships = forms.ModelMultipleChoiceField(
        label="Do you intend to apply for fellowships and/or assistantships?",
        queryset = FELLOWSHIPS,
        help_text = 'Check all that apply',
        widget = forms.CheckboxSelectMultiple(),
        required=False
    )
    gdpr = forms.TypedChoiceField(
        label="""Are you currently located in a European Union country,
            Iceland, Liechtenstein, Norway, or Switzerland?
        """, choices=BINARY_CHOICES, widget=forms.RadioSelect()
    )
    audition_date = forms.ModelChoiceField(
        label="Please choose an audition date",
        queryset=DATES,
        required=False,
    )
    audition_time = forms.ModelChoiceField(
        label="Please choose preferred audition time block",
        queryset=TIMES,
        required=False,
    )
    payment_method = forms.TypedChoiceField(
        choices=PAYMENT_CHOICES, widget=forms.RadioSelect(),
    )
    payment_waiver = forms.CharField(required=False)

    class Meta:
        model = Application
        exclude = ('slug','entry_term','social_security_four')

    def clean(self):

        cd = self.cleaned_data
        if cd.get('gre') == 'Yes':
            if not cd.get('gre_date'):
                self.add_error('gre_date', "Required field")
            if not cd.get('gre_score'):
                self.add_error('gre_score', "Required field")
        if cd.get('gmat') == 'Yes':
            if not cd.get('gmat_date'):
                self.add_error('gmat_date', "Required field")
            if not cd.get('gmat_score'):
                self.add_error('gmat_score', "Required field")
        if cd.get('gdpr') == 'Yes':
            if not cd.get('gdpr_cookies'):
                self.add_error('gdpr_cookies', "Required field")
            if not cd.get('gdpr_transfer'):
                self.add_error('gdpr_transfer', "Required field")
            if not cd.get('gdpr_collection'):
                self.add_error('gdpr_collection', "Required field")
        code = cd.get('payment_waiver')
        if cd.get('payment_method') == 'Waiver Code':
            if code:
                valid = GenericChoice.objects.filter(value=code).filter(
                    tags__name=settings.ADMISSIONS_WAIVER_CODE_TAG,
                )
                if not valid:
                    self.add_error('payment_waiver', "Invalid waiver code")
            else:
                self.add_error('payment_waiver', "Please provide a waiver code")
        return cd


class ContactForm(forms.ModelForm):
    """
    Continuing Studies admissions application contact form
    """

    class Meta:
        model = Contact
        fields = ('first_name','last_name','email')


class EducationForm(forms.ModelForm):
    """
    Continuing Studies admissions application education form
    """

    class Meta:
        model = School
        exclude = ('application',)


class EducationRequiredForm(forms.ModelForm):
    """
    Continuing Studies admissions application education form
    """

    name = forms.CharField(
        required=True, max_length=255
    )
    state = forms.CharField(
        label="State/Province", required=True, max_length=50
    )
    degree = forms.CharField(
        label="Diploma/Degree", required=True, max_length=255
    )
    attended = forms.CharField(
        label="Dates Attended", required=True, max_length=255
    )
    majorminor = forms.CharField(
        label="Major(s)/Minor(s)", required=True, max_length=255
    )
    gpa = forms.DecimalField(
        label="GPA", required=True, max_digits=4, decimal_places=2
    )

    class Meta:
        model = School
        exclude = ('application',)


class OrderForm(OrderForm):
    """
    Credit Card transaction form
    """
    total = forms.CharField(
        label="Application Fee",
    )

    class Meta:
        model = Order
        fields = ('total','avs','auth')
