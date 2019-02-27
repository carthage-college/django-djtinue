from django import forms
from django.conf import settings

from djtinue.admissions.application.models import Application

from djtools.fields import GENDER_CHOICES, BINARY_CHOICES, PAYMENT_CHOICES

from localflavor.us.forms import USPhoneNumberField, USZipCodeField
from localflavor.us.forms import USSocialSecurityNumberField

CHOICES = (
    ('',""),
)


class ApplicationForm(forms.ModelForm):
    """
    Continuing Studies admissions application form submission
    """

    class Meta:
        model = Application
        fields = __all__

