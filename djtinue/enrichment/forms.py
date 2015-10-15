from django import forms

from djtinue.enrichment.models import Registration

from djtools.fields import BINARY_CHOICES
from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm
from djforms.core.models import REQ, STATE_CHOICES

from localflavor.us.forms import USPhoneNumberField, USZipCodeField
from localflavor.us.forms import USSocialSecurityNumberField


class RegistrationForm(ContactForm):
    """
    Registration form for enrichment courses
    """

    previous_name = forms.CharField(
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
        widget=forms.TextInput(attrs=REQ)
    )
    phone_home = USPhoneNumberField(
        label = "Home phone",
        widget=forms.TextInput(attrs=REQ)
    )
    phone_work = USPhoneNumberField(
        label = "Work phone",
        required=False
    )
    email = forms.EmailField(label='Personal email')
    email_work = forms.EmailField(label='Work email')
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

    def clean(self):
        cd = super(RegistrationForm, self).clean()
        attended_before = cd.get("attended_before")
        collegeid = cd.get("collegeid")

        if attended_before == "Yes" and collegeid == "":
            self._errors["collegeid"] = self.error_class(
                ["Required field."]
            )

        return cd

    class Meta:
        model = Registration
        fields = (
            'first_name','second_name','last_name','previous_name',
            'address1','city','state','postal_code','phone','date_of_birth',
            'phone_home','phone_work','email','email_work','attended_before',
            'social_security_number', 'collegeid','verify'
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

