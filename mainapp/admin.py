from django.contrib import admin

# Register your models here.

from .models import formpublicdata,responses,formMCQquestions


admin.site.register(formpublicdata)

admin.site.register(responses)

admin.site.register(formMCQquestions)

admin.site.site_header = "Login to Developer Nested Form"
admin.site.site_title = "Welcome to Admin Panel NestedForms"
admin.site.index_title = "Developed by Mohit Satija"
