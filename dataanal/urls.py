from django.urls import path
from .views import *

urlpatterns = [
    path('createcsv',Create_Csv_User_Marks_Api),
    path('createcsvform',Create_Csv_Resp_forms),
]
