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
        'verify', 'courses', 'order'
    )
    search_fields = ('last_name', 'email','social_security_number')
    ordering = ['-created_at',]
    #inlines = (OrderInline,)
    raw_id_fields = ("order",)

admin.site.register(Course, CourseAdmin)
admin.site.register(Registration, RegistrationAdmin)
