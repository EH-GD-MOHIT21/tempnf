from django.urls import path
from .views import *


urlpatterns = [
    path('createquiz',RenderCreateQuiz),
    path('savequiz',SaveQuiz),
    path('fillquiz/<quiz_id>',FillQuiz),
    path('savequiz/<quiz_id>',SaveQuizResposnes),
    path('managequizes',ManageQuizes),
    path('showquizresponses/<quiz_id>/filter',showresponses)
]
