#I need all the imports below
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic

from djtinue.masters.models import AdultEdModel
from djtinue.masters.forms import AdultEdForm
from datetime import date
# Create your views here.
def index(request):
    year = date.today().year
    if date.today().month <= 5:
            year = year - 1
    if request.method == 'POST': # If the form has been submitted...
        form = AdultEdForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save() #Save the data
            form = AdultEdForm()
            submitted = True
            return render(request, 'masterseducation/form.html', {
                'form': form,
                'submitted': submitted,
                'year_low': year,
                'year_up': year+1
            })
    else:
        form = AdultEdForm() # An unbound form

    return render(request, 'masterseducation/form.html', {
        'form': form,
        'year_low': year,
        'year_up': year+1
    })
