from django import forms
from django.utils.safestring import mark_safe

from djtinue.enrichment.models import Registration

from djtools.fields import BINARY_CHOICES
from djtools.fields.localflavor import USPhoneNumberField
from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm
from djforms.core.models import REQ, STATE_CHOICES

from localflavor.us.forms import USSocialSecurityNumberField, USZipCodeField


class RegistrationForm(ContactForm):
    """Registration form for enrichment courses."""

    previous_name = forms.CharField(
        label = "Previous Last Name",
        max_length=128,
        required=False
    )
    address1 = forms.CharField(
        label = "Address",
        max_length=255,widget=forms.TextInput(attrs=REQ)
    )
    city = forms.CharField(
        max_length=128,widget=forms.TextInput(attrs=REQ)
    )
    state = forms.CharField(
        widget=forms.Select(choices=STATE_CHOICES, attrs=REQ)
    )
    postal_code = USZipCodeField(
        label="Zip code",
        widget=forms.TextInput(
            attrs={'class': 'required input-small','maxlength':'5'}
        )
    )
    phone = USPhoneNumberField(
        label = "Mobile phone",
        required = False,
    )
    phone_home = USPhoneNumberField(
        label = "Home phone",
        required = False,
    )
    phone_work = USPhoneNumberField(
        label = "Work phone",
        required=False
    )
    email_work = forms.EmailField(label='Work email', required=False)
    email = forms.EmailField(label='Personal email', required=False)
    social_security_number = USSocialSecurityNumberField(
        max_length=11
    )
    date_of_birth = forms.DateField(
        label="Birthdate"
    )
    attended_before = forms.TypedChoiceField(
        label = "Have you attended Carthage in the past?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect()
    )
    gdpr = forms.TypedChoiceField(
        label = """Are you currently located in a European Union country,
            Iceland, Liechtenstein, Norway, or Switzerland?
        """, choices=BINARY_CHOICES, widget=forms.RadioSelect()
    )

    class Meta:
        model = Registration
        fields = (
            'first_name','second_name','last_name','previous_name',
            'address1','city','state','postal_code','phone','date_of_birth',
            'phone_home','phone_work','email_work','email','attended_before',
            'gdpr','gdpr_cookies','gdpr_transfer','gdpr_collection',
            'social_security_number','collegeid','verify'
        )


class RegistrationOrderForm(OrderForm):
    """
    """
    total = forms.CharField(
        label="Registration Fee",
    )

    class Meta:
        model       = Order
        fields      = ('total','avs','auth')

    def clean(self):
        cd = self.cleaned_data
        if int(cd["total"]) <= 10:
            raise forms.ValidationError(mark_safe(
                """
                <p>
                Please verify that you have chosen at least one course. If
                you have done so and still see this error, please contact
                the contact
                <a href="mailto:ocs@carthage.edu">The Office of Continuing Studies</a> |
                <a href="tel:262.551.5924">262.551.5924</a>.
                </p>
                """
            ))
        return cd
