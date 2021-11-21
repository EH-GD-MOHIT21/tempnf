from django.urls import path
from .views import *

urlpatterns = [
    path('survey/<quiz_id>',RenderSurveyForQuiz),
]
