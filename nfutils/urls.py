from django.urls import path
from .views import ReleaseQuizScoreApi

urlpatterns = [
    path('releasescore',ReleaseQuizScoreApi),
]
