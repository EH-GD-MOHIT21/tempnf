from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(QuizManager)
admin.site.register(QuizMCQquestions)
admin.site.register(QuizFillTypeQuestions)
admin.site.register(QuizMCQAnswers)
#responses
admin.site.register(base_submitted_form_data)
admin.site.register(FillTypeUserResponses)
admin.site.register(MCQTypeUserResponses)