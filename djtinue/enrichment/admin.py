from django.contrib import admin
from djtinue.enrichment.models import Course, Registration

class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = (
        'title', 'course_number', 'credits', 'room', 'active'
    )
    ordering = ['active','title','course_number']

    class Media:
        js = [
            '/static/djtinue/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/djtinue/grappelli/tinymce_setup/tinymce_setup.js',
        ]

class OrderInline(admin.TabularInline):
    model = Registration.order.through
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


class RegistrationAdmin(admin.ModelAdmin):
    model = Registration
    list_display = (
        'first_name', 'last_name', 'email','created_at'
    )
    fields = (
        'first_name', 'second_name', 'last_name', 'previous_name',
        'address1', 'city', 'state', 'postal_code',
        'phone', 'phone_home', 'phone_work',
        'email_work', 'email', 'social_security_number',
        'date_of_birth', 'attended_before', 'collegeid',
        'verify', 'courses'
    )
    search_fields = ('last_name', 'email','social_security_number')
    ordering = ['-created_at',]
    raw_id_fields = ("order",)
    exclude = ('order',)
    inlines = [
        OrderInline,
    ]


admin.site.register(Course, CourseAdmin)
admin.site.register(Registration, RegistrationAdmin)
