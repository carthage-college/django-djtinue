from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic

from djtinue.graduate.candidicy.models import Application
from djtinue.graduate.candidicy.forms import ApplicationForm

from datetime import date

def index(request):
    year = date.today().year
    if date.today().month <= 5:
        year = year - 1
    if request.method == 'POST': # If the form has been submitted...
        form = ApplicationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save() #Save the data
            return HttpResponseRedirect(reverse(""))
    else:
        form = AdultEdForm() # An unbound form

    return render(request, 'masterseducation/form.html', {
        'form': form,
        'year_low': year,
        'year_up': year+1
    })
