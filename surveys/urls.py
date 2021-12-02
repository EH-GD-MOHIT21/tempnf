from django.urls import path
from .views import *

urlpatterns = [
    path('survey/<quiz_id>',RenderSurveyForQuiz),
    path('surveyform/<form_id>',RenderSurveyForForm),
    path('creatoraccesspage',RenderDashboard),
    path('updatetimeinterval',commonAPIsetNewOpenCloseTime),
    path('updatetime/<form_id>',RenderUpdateTime),
]
