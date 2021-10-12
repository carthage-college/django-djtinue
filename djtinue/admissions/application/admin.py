# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from djtinue.admissions.application.forms import RACES
from djtinue.admissions.application.models import Application
from djtinue.admissions.application.models import Contact
from djtinue.admissions.application.models import School


class SchoolInline(admin.StackedInline):
    """Admin class that allows us to display schools in line."""

    model = School
    can_delete = True
    max_num = 5
    fields = (
        'state',
        'degree',
        'attended',
        'majorminor',
        'gpa',
        'transcript',
    )
    show_change_link = True
    verbose_name = 'School'
    verbose_name_plural = 'Schools'


class ContactInline(admin.TabularInline):
    """Admin class that allows us to display contacts in line."""

    model = Contact
    max_num = 2
    can_delete = False
    fields = ('last_name', 'first_name', 'email')
    show_change_link = True
    verbose_name = 'Recommentation'
    verbose_name_plural = 'Recommentations'


class OrderInline(admin.TabularInline):
    """Admin class that allows us to display orders in line."""

    model = Application.order.through
    verbose_name_plural = 'Payment Information'
    max_num = 1
    exclude = ['order']
    readonly_fields = (
        'cc_name',
        'cc_four_digits',
        'total',
        'status',
        'transid',
    )
    can_delete = False

    def cc_name(self, instance):
        """Display the name on the credit card."""
        return instance.order.cc_name
    cc_name.short_description = 'Name on card'

    def cc_four_digits(self, instance):
        """Disply the last four digits of the credit card."""
        return 'x{0}'.format(instance.order.cc_four_digits)
    cc_four_digits.short_description = 'Last 4 digits on card'

    def total(self, instance):
        """Display the order total."""
        return instance.order.total
    total.short_description = 'Total'

    def status(self, instance):
        """Display the order status."""
        return instance.order.status
    status.short_description = 'Status'

    def transid(self, instance):
        """Display the order transaction ID."""
        return instance.order.transid
    transid.short_description = 'Transaction ID'


class ApplicationForm(forms.ModelForm):
    """Admin form class for the continuing studies application."""

    phone = forms.CharField(label='Home Phone')
    race = forms.ModelMultipleChoiceField(
        queryset=RACES,
        help_text='Check all that apply',
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        """Sub-class for establishing settings on the parent class."""

        model = Application
        fields = '__all__'


class ApplicationAdmin(admin.ModelAdmin):
    """Admin class for the continuing studies application."""

    form = ApplicationForm
    list_display = (
        'last_name',
        'first_name_print',
        'email',
        'created_at',
        'viewed',
    )
    search_fields = ('last_name', 'email', 'social_security_number')
    ordering = ('-created_at', 'last_name')
    list_editable = ['viewed']
    raw_id_fields = ['order']
    exclude = ['order']
    inlines = (OrderInline, ContactInline, SchoolInline)

    class Media:
        """Sub-class for declaring static files for display in admin."""

        css = {
            'all': ('/static/djtinue/css/admin.css',),
        }

    def first_name_print(self, instance):
        """Display the given name as a link to print view."""
        return mark_safe('<a href="{0}" target="_blank">{1}</a>'.format(
            reverse(
                'admissions_application_detail',
                kwargs={'aid': instance.id},
            ),
            instance.first_name,
        ))
    first_name_print.allow_tags = True
    first_name_print.short_description = 'First Name (print)'


admin.site.register(Application, ApplicationAdmin)
admin.site.register(Contact)
admin.site.register(School)
