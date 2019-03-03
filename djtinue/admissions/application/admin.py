from django import forms
from django.contrib import admin
from django.utils import timezone

from djtinue.admissions.application.models import Application
from djtinue.admissions.application.forms import RACES


class OrderInline(admin.TabularInline):
    model = Application.order.through
    max_num = 1
    exclude = ('order',)
    readonly_fields = [
        'cc_name','cc_4_digits','total','status','transid'
    ]
    can_delete = False

    def cc_name(self, instance):
        return instance.order.cc_name
    cc_name.short_description = 'Name on card'

    def cc_4_digits(self, instance):
        return "x{}".format(instance.order.cc_4_digits)
    cc_4_digits.short_description = 'Last 4 digits on card'

    def total(self, instance):
        return instance.order.total
    total.short_description = 'Total'

    def status(self, instance):
        return instance.order.status
    status.short_description = 'Status'

    def transid(self, instance):
        return instance.order.transid
    transid.short_description = 'Transaction ID'


class ApplicationForm(forms.ModelForm):
    phone = forms.CharField(label="Home Phone")
    race = forms.ModelMultipleChoiceField(
        queryset = RACES,
        help_text = 'Check all that apply',
        widget = forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Application
        fields = '__all__'


class ApplicationAdmin(admin.ModelAdmin):
    form =  ApplicationForm
    list_display = (
        'last_name', 'first_name', 'email','created_at','viewed'
    )
    search_fields = ('last_name', 'email','social_security_number')
    ordering = ['-created_at','last_name']
    list_editable = ('viewed',)
    raw_id_fields = ('order',)
    exclude = ('order',)
    inlines = [
        OrderInline,
    ]

    class Media:
        css = {
            'all': (
                '/static/djtinue/css/admin.css',
            )
        }

admin.site.register(Application, ApplicationAdmin)
