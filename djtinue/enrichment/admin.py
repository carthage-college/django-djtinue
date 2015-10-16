from django.contrib import admin
from djtinue.enrichment.models import Course, Registration

class CourseAdmin(admin.ModelAdmin):
    model = Course


class CourseInline(admin.TabularInline):
    model = Registration.courses.through
    #fields = ('title', 'abstract',)


class RegistrationAdmin(admin.ModelAdmin):
    model = Registration
    list_display = (
        'first_name', 'last_name', 'email','created_at'
    )
    search_fields = ('last_name', 'email',)
    ordering = ['-created_at',]
    #inlines = (CourseInline,)
    raw_id_fields = ("order",)

admin.site.register(Course, CourseAdmin)
admin.site.register(Registration, RegistrationAdmin)
