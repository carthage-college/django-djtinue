#admin.py is where we create 'actions' that users can do to entries
#within this app, masterseducation, as well as settings to change how
#we view entries within 'masterseducation'

#'admin' - necessary to change view settings when viewing an 'masterseducation' object
#'messages' - necessary to change success/fail messages when performing an action to an 'masterseducation' object
from django.contrib import admin, messages
from djtinue.masters.models import AdultEdModel
import re #For RegexValidation
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine

#This is an 'action' a user can perform to a 'masterseducation' object
def push_to_production(modeladmin, request, queryset):
    push_to_production.short_description = 'Push to production server' #What the user sees

    # This is the bulk of moving data from the development to production databases
    #
    # *Understand this first - The data that exists in the form will be moved to separate
    # tables in the production server. Some fields might be moved to table 'A', others to table
    # 'B', and the rest might go to table 'C'. 
    # 
    # Steps to accomplish this:
    # 1) Find all of the tables where your data will be moving when it goes to the production
    # server. 
    #
    # 2) Download MySQLWorkbench and make copies of the tables on your local machine you found in step 1.
    # Be sure to copy the structure of the table exactly as found on the production server (including the name of the table)
    #
    # 3) Run this command and be sure 'newmodels.py' has been created in your project
    # (Run the command while within the 'root' project folder on your local machine. This
    # assumes you have been developing the form on your local machine)
    #       python manage.py inspectdb --database=default2 > newmodels.py
    #
    #   *Note: 'default2' is the name of your database where you have created the tables in
    #   step 2. This database should be a copy of the production database on the server (at the very least a copy of the tables you will need from step 1)
    #   This is found in the project's 'settings.py' file
    #
    # 4) On the top of this page, import the 'newmodels.py' file
    #
    # 5) Look in 'newmodels.py', you will see a bunch of classes. Each class represents a 
    # table. Now look at the fields in each class. For the below sample code, assume you had two classes
    # in 'newmodels.py' named 'table_one' and 'table_two'
    #
    #   'table_one' has these fields:
    #       id, name, tel
    #
    #   'table_two' has these fields:
    #       id, address
    #
    #   Also assume that your form has these fields:
    #       my_id, form, phone_number
    #
    # 6) For each class, use some code like below to save the data to your production database (keep this code in the function this comment is in)
    # *Note: replace 'default2' with the name YOU used for your production database (in 'settings.py')
    # *Note: feel free to un-comment the code below and make changes you need, you can keep these comments for reference
    # *Note: .get_or_create() makes an object if one is not found or updates an existing one if found
    # *Note: 'created' is a boolean that is true if an object was created from .get_or_create()
    # *Note: .save() saves the data to the production server
    # *Note: parameters within .get_or_create() are ... .get_or_create(field_from_newmodels.py=each.field_in_my_form)
    #
    #   for each in queryset: #Loops through all instances of the form object
    #       (obj, created) = table_one.objects.using('default2').get_or_create(id=each.my_id,name=each.name,tel=each.phone_number)
    #       obj.save()
    #       (obj, created) = table_two.objects.using('default2').get_or_create(id=each.my_id,address=each.address)
    #       if not obj.address:
    #           #You can also use 'warning', 'debug', 'info' and 'success' in place of 'error'
    #           messages.error(request, 'Object did not have an address')
    #       obj.save()
    #       messages.success(request, 'Object was moved to production!')
    #



#def push_to_databases(modeladmin, request, queryset):
#    for item in queryset:
#    
#        if item.phone_number:
#            (obj, created) = AaRec.objects.using('default2').get_or_create(id=item.student_id, phone=item.phone_number, aa='CELL')
#            obj.save()
#        if item.email:
#            if re.search('^.*@carthage\.edu$', item.email) != None:
#                (obj, created) = AaRec.objects.using('default2').get_or_create(id=item.student_id, aa='EML1', line1=item.email) #carthage email
#            else:
#                (obj, created2) = AaRec.objects.using('default2').get_or_create(id=item.student_id, aa='EML2', line1=item.email) #non carthage email
#            obj.save()
#        if item.address:
#            (obj, created2) = AaRec.objects.using('default2').get_or_create(id=item.student_id, aa='MAIL', city=item.city, st=item.state, zip=item.zip)
#            obj.save()
            

        
#        (obj2, created2) = AcadRec.objects.using('default2').get_or_create(id=item.student_id)
#        obj2.conc1=item.concentration
#        obj2.save()
        
        
#        (obj3, created3) = GradwalkRec.objects.using('default2').get_or_create(id=item.student_id)
#        obj3.plan2walk=item.participate_in_ceremony
#        obj3.name_on_diploma="%s %s %s" % (item.first_name, item.middle_name, item.last_name)
        
#        if obj3.plan2walk:
#            obj3.plan2walk = 'y'
#        else:
#            obj3.plan2walk = 'n'
        
#        obj3.save()
        
#        (obj4, created4) = IdRec.objects.using('default2').get_or_create(id=item.student_id)

#        obj4.firstname=item.first_name
#        obj4.middlename=item.middle_name
#        obj4.lastname=item.last_name
#        obj4.fullname="%s %s %s" % (item.first_name, item.middle_name, item.last_name)
#        obj4.addr_line1=item.address
#        obj4.city=item.city
#        obj4.st=item.state
#        obj4.zip=item.zip
#        obj4.phone=item.phone_number
        
#        obj4.save()


class AdultEdAdmin(admin.ModelAdmin):
    search_fields = ['participate_in_ceremony']    
    list_display = ('first_name', 'student_id', 'participate_in_ceremony') #We will only see the following fields as columns in the admin page
    fieldsets = ( #How the 'masterseducation' object is displayed in the editor in the admin page
        ('Student Info', {
            'fields': ('student_id','first_name','last_name','concentration','participate_in_ceremony') 
        }),
        ('Other information', {
            'classes': ('collapse',), #Makes this header collapsible
            'fields': ('phone_number','email','address','city','state','zip') #These two fields will be under the parent header 'Application Information'
        })
    )
    actions = [push_to_production] #Includes the action we defined earlier in this page

admin.site.register(AdultEdModel, AdultEdAdmin)

