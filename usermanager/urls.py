from django.urls import path
from . import views

urlpatterns = [
    path('register',views.RenderSignup),
    path('login',views.RenderLogin),
    path('logmeout',views.logoutview),
    path('generateotp',views.sendOtp),
    path('login/setcache',views.logusertocache),
    path('login/verify',views.loginuser),
    path('register/setcache',views.RegisterUsertoCache),
    path('register/verify',views.verifyRegisterUser),
    path('forgetpass',views.RenderFP),
    path('forgotpassApi',views.forgotpasscachegen),
    path('user=<email>/token=<token>',views.Renderresetpassword),
    path('changepass/user=<email>/token=<token>',views.ChangePass),
    path('isstrongpass',views.StrongPassOrNot),
]