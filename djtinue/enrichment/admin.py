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


class CourseInline(admin.TabularInline):
    model = Registration.courses.through
    #fields = ('title', 'abstract',)


class RegistrationAdmin(admin.ModelAdmin):
    model = Registration
    list_display = (
        'first_name', 'last_name', 'email','created_at'
    )
    search_fields = ('last_name', 'email','social_security_number')
    ordering = ['-created_at',]
    #inlines = (CourseInline,)
    raw_id_fields = ("order",)

admin.site.register(Course, CourseAdmin)
admin.site.register(Registration, RegistrationAdmin)
