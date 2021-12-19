
from django.urls import path
from . import views


urlpatterns = [
    path('',views.home),
    path('fillform',views.fillform),
    path('createform',views.createform),
    path('savedetails',views.savedetails),
    path('fillform/<slug:formid>',views.fillform),
    path('saveresponse/<slug:formid>',views.saveresponse),
    path('getformbyid',views.getformbyid),
    path('fillformuser',views.fillformuser),
    path('showresponses/<slug:formid>/filter',views.showresponsepage),
    path('manageforms',views.creatorpageview),
    path('updateformperm',views.set_form_res_visibility_Api),
    path('deleteform',views.delete_form_api),
    path('delformresponse',views.delete_form_response_api),
    path('setacpformrespapi',views.set_form_acpres_Api),
    path('manageformresponses/<form_id>',views.ExpendResponseForm),
    path('getresform/<form_id>',views.SendFormResData),
]
