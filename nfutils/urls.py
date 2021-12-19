from django.urls import path
from .views import ReleaseQuizScoreApi, RenderUpdateForm, UpdateForm, delformftp,delmcqform

urlpatterns = [
    path('releasescore',ReleaseQuizScoreApi),
    path('updateform/<form_id>',RenderUpdateForm),
    path('setupdateform/<form_id>',UpdateForm),
    path('delmcqform',delmcqform),
    path('delftpform',delformftp),
]
