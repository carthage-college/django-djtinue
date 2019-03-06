from django import forms
from django.conf import settings

from djtinue.admissions.application.models import Application, Contact, School

from djtools.fields import BINARY_CHOICES, GENDER_CHOICES, PAYMENT_CHOICES, TODAY
from djforms.processors.models import Order
from djforms.core.models import GenericChoice, GenericContact
from djforms.processors.forms import OrderForm

RACES = GenericChoice.objects.filter(tags__name__in=['Race']).order_by('ranking')

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
        label="State/Provence",
        max_length=128, required=True
    )
    postal_code = forms.CharField(
        label="Postal code",
        max_length=10, required=True
    )
    phone = forms.CharField(
        label="Home phone",
        max_length=16, required=True
    )
    phone_secondary = forms.CharField(
        label="Work phone",
        max_length=16, required=True
    )
    phone_tertiary = forms.CharField(
        label="Cell phone",
        max_length=16, required=True
    )
    social_security_number = forms.CharField(
        label="Social Security or National Identity number",
        max_length=16, required=True
    )
    latinx = forms.TypedChoiceField(
        label="Are you Hispanic or Latino?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect()
    )
    race = forms.ModelMultipleChoiceField(
        queryset = RACES,
        help_text = 'Check all that apply',
        widget = forms.CheckboxSelectMultiple()
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
    fellowships = forms.TypedChoiceField(
        label="Do you intend to apply for fellowships and/or assistantships?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect()
    )
    gdpr = forms.TypedChoiceField(
        label="""Are you currently located in a European Union country,
            Iceland, Liechtenstein, Norway, or Switzerland?
        """, choices=BINARY_CHOICES, widget=forms.RadioSelect()
    )
    payment_method = forms.TypedChoiceField(
        choices=PAYMENT_CHOICES, widget=forms.RadioSelect(),
    )

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
