from django import forms
from django.core import validators #Need this one for validators
from djtinue.masters.models import AdultEdModel

# Create your models here.
class AdultEdForm(forms.ModelForm):
    
    #I need this constructor to change validators
    def __init__(self, *args, **kwargs):
        super(AdultEdForm, self).__init__(*args,**kwargs)
        
        #Validate a bunch of fields / change labels below
        self.fields['student_id'].validators = [validators.RegexValidator(regex=('^[\d]{5,7}$'),message='Not a valid 5-7 digits Carthage id',code='a')] #Note*: 'code' can be anything except 'invalid'
        self.fields['first_name'].validators = [validators.RegexValidator(regex=('^[a-zA-Z\']+[a-zA-Z\\-\\s\']+$'),message='Not a valid first name',code='a')] #'message' is what shows up if the field fails validation
        self.fields['middle_name'].validators = [validators.RegexValidator(regex=('^[a-zA-Z\']+[a-zA-Z\\-\\s\']+$'),message='Not a valid middle name',code='a')]
        self.fields['last_name'].validators = [validators.RegexValidator(regex=('^.+$'),message='Not a valid last name',code='a')]
        self.fields['concentration'].validators = [validators.RegexValidator(regex=('^.+$'),message='Not a concentration',code='a')]
        self.fields['phone_number'].label = 'Phone number'
        self.fields['phone_number'].validators = [validators.RegexValidator(regex=('^(\d{4}|\d{3}[\s\-\.]?\d{4}|1?[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4})$'),message='Use this format: xxx-xxx-xxxx',code='a')]
        self.fields['email'].validators = [validators.RegexValidator(regex=('^[A-Za-z0-9_]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,4}$'),message='Not a valid email address',code='a')]
        self.fields['address'].validators = [validators.RegexValidator(regex=('^.+$'),message='Not a valid address',code='a')]
        self.fields['city'].validators = [validators.RegexValidator(regex=('^.+$'),message='Not a valid city',code='a')]
        self.fields['state'].validators = [validators.RegexValidator(regex=('^[a-zA-Z]{2}$'),message='Use this format: xx',code='a')]
        self.fields['zip'].validators = [validators.RegexValidator(regex=('^[\d]{5}$'),message='Use this format: xxxxx',code='a')]
    
    #Global options    
    class Meta:
        model = AdultEdModel #Set the forms to the fields in 'AdultEdModel'

