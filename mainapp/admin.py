from django.contrib import admin

# Register your models here.

from .models import formpublicdata,formMCQquestions,formFillTypeQuestions,base_form_data_response,formFillTypeResponse,formMCQTypeResponse


admin.site.register(formpublicdata)

admin.site.register(formMCQquestions)

admin.site.register(formFillTypeQuestions)

admin.site.register(base_form_data_response)

admin.site.register(formMCQTypeResponse)

admin.site.register(formFillTypeResponse)

admin.site.site_header = "Login to Developer Nested Form"
admin.site.site_title = "Welcome to Admin Panel NestedForms"
admin.site.index_title = "Developed by Mohit Satija"
