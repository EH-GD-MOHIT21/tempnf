from django.urls import path
from .views import *


urlpatterns = [
    path('createquiz',RenderCreateQuiz),
    path('savequiz',SaveQuiz),
    path('fillquiz/<quiz_id>',FillQuiz),
    path('savequiz/<quiz_id>',SaveQuizResposnes),
    path('managequizes',ManageQuizes),
    path('showquizresponses/<quiz_id>/filter',showresponses),
    path('updatemark',update_mark_filltype_Api),
    path('deletequiz',delete_quiz_api),
    path('deluserresponse',delete_response_api),
    path('updatequizperm',set_quiz_res_visibility_Api),
    path('changeacceptrespapi',set_accepting_respquiz_api),
    path('managequizresponses/<quiz_id>',ExpendResponseQuiz),
    path('getresquiz/<quiz_id>',SendQuizResData),
]
