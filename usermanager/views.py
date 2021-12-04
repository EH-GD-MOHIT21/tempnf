from django.shortcuts import redirect, render
from django.contrib.auth import login,authenticate, logout
from .app_utils.data_handler import *
from .app_utils.mailer import *
from .app_utils.verification import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.cache import cache
import json
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
# Create your views here.


def loginview(request):
    if request.method == "POST" and (not request.user.is_authenticated):
        pass
    return redirect('/')

def RenderFP(request):
    return render(request,'forgetpass.html')

def logoutview(request):
    logout(request)
    return redirect('/')

def RenderLogin(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
    return redirect('/')

def RenderSignup(request):
    if not request.user.is_authenticated:
        return render(request,'register.html')
    return redirect('/')

@csrf_exempt
def sendOtp(request):
    otp = GenerateOTP()
    try:
        Fetch_cache(request.data["username"])
        return JsonResponse({'status':406,'message':'otp send please try after 5 minutes.'})
    except Exception as e:
        pass
    value = send_mail(to=request.data["username"],subject="Welcome User to Nested Forms.",message=f"Your otp is {otp} valid for 5 minutes. Thanks\n\nRegards NestedForms.\nHappy Form Creating.")
    if value:
        cache.set(request.data["username"],otp,timeout=300)
        return JsonResponse({'status':200,'message':'Otp send on provided Mail Id.'})
    else:
        return JsonResponse({'status':500,'message':'Err: Human Validation Failed due to Empty Recaptcha Provided.'})

@csrf_exempt
def RegisterUsertoCache(request):
    if request.method == "POST":
        data = json.loads(request.body)
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        cpass = data.get("cpassword")
        # print(first_name,last_name,username,email,password,cpass,sep='\n')
        try:
            Fetch_cache(email)
            return JsonResponse({'status':400,'message':'Otp Already send please wait for 5 minutes for resend.'})
        except:
            pass
        if not isValidName(first_name):
            return JsonResponse({'status':406,'message':'Invalid first Name.'})
        if not isValidName(last_name):
            return JsonResponse({'status':406,'message':'Invalid last Name.'})
        if not isValidMail(username) or not isValidMail(email):
            return JsonResponse({'status':406,'message':'Invalid mail id.'})
        try:
            User.objects.get(username=username)
            return JsonResponse({'status':406,'message':'Email or username already exists.'})
        except:
            pass
        status,message = isValidPass(password,cpass)
        if not status:
            return JsonResponse({'status':406,'message':f'{message}'})

        otp = GenerateOTP()
        set_cache({"first_name":first_name,"last_name":last_name,"email":email,"password":password},otp)
        value = send_mail(to=email,subject="Welcome User to Nested Forms.",message=f"Your otp is {otp} valid for 5 minutes. Thanks\n\nRegards NestedForms.\nHappy Form Creating.")
        if value:
            return JsonResponse({'status':200,'message':'otp send.'})
        else:
            return JsonResponse({'status':500,'message':'Err: Human Validation Failed due to Empty Recaptcha Provided please try after 5 minutes.'})
    else:
        return JsonResponse({'status':400,'message':'Invalid Request.'})

@csrf_exempt
def loginuser(request):
    if request.method == "POST" and not request.user.is_authenticated:
        try:
            pdata = json.loads(request.body)
            data = Fetch_cache(pdata.get("username"))
            otpuser = pdata.get("otp")
            password = pdata.get("password")
            otp = data["otp"]
            if str(otpuser).strip() != str(otp).strip():
                return JsonResponse({'status':406,'message':'Invalid Otp'})
        except Exception as e:
            print("Exception is ",e)
            return JsonResponse({'status':404,'message':'User Not Exist or session expired.'})
        try:
            user = User.objects.get(username=pdata.get("username"))
            if check_password(password,user.password):
                login(request,user)
                delete_pattern(pdata.get("username"))
                # print('yes done with backend.')
                return JsonResponse({'status':200,'message':'success'})
            else:
                return JsonResponse({'status':404,'message':'Invalid Username or Password.'})
        except Exception as e:
            print(e)
            return JsonResponse({'status':404,'message':'User Not Exist or session expired.'})

    else:
        return redirect('/')

@csrf_exempt
def logusertocache(request):
    print("before setting",cache._cache.keys())
    if request.method == 'POST' and not request.user.is_authenticated:
        body = json.loads(request.body)
        username = body.get("username")
        password = body.get("password")
        user = authenticate(username=username,password=password)
        if user!=None:
            try:
                Fetch_cache(username)
                return JsonResponse({'status':406,'message':'otp send please try after 5 minutes.'})
            except ValueError:
                pass
            except Exception as e:
                raise(e)
                print("Exception is: ",e)
                pass
            otp = GenerateOTP()
            cache.set(username,{"password":password,"otp":otp},timeout=300)
            print("after setting",cache._cache.keys())
            value = send_mail(to=username,subject="Welcome User to Nested Forms.",message=f"Your otp is {otp} valid for 5 minutes. Thanks\n\nRegards NestedForms.\nHappy Form Creating.")
            
            if value:
                return JsonResponse({'status':200,'message':'otp send.'})
            else:
                return JsonResponse({'status':500,'message':'Err: Human Validation Failed due to Empty Recaptcha Provided please try after 5 minutes.'})
        else:
            return JsonResponse({'status':404,'message':'Invalid UserName or password.'})
    else:
        return JsonResponse({'status':400,'message':'Invalid Request.'})



@csrf_exempt
def verifyRegisterUser(request):
    if request.method == "POST" and not request.user.is_authenticated:
        body = json.loads(request.body)
        email = body.get("email")
        otp = body.get("otp")
        print("before deleting: ",cache._cache.keys())
        try:
            data = Fetch_cache(email)
            if str(otp).strip() == str(data["otp"]).strip():
                user = User()
                user.first_name = data["first_name"]
                user.last_name = data["last_name"]
                user.email = email
                user.username = email
                user.set_password(data["password"])
                user.save()
                delete_pattern(email)
                print("after deleting",cache._cache.keys())
                return JsonResponse({'status':200,'message':'success'})
            else:
                return JsonResponse({'status':406,'message':'Invalid otp.'})
        except Exception as e:
            print(e)
            print("after deleting",cache._cache.keys())
            return JsonResponse({'status':403,'message':'Session Expired For User Please Try Again.'})
    else:
        return JsonResponse({'status':400,'message':'Invalid Request.'})


@csrf_exempt
def forgotpasscachegen(request):
    try:
        body = json.loads(request.body)
        email = str(body.get("email"))
    except:
        return JsonResponse({'status':400,'message':'Invalid Request.'})

    try:
        Fetch_cache(email)
        return JsonResponse({'status':406,'message':'Looks Like You already have pending request please wait for 5 minutes before retry.'})
    except:
        pass

    try:
        user = User.objects.get(username=email)
        slug = GenerateSlug()
        uri = settings.SITE_URL
        path = str(uri)+f"user={email}/"+f"token={slug}"
        value = send_mail(to=email,subject="Welcome User to Nested Forms.",message=f"Your password reset link is {path} valid for 5 minutes. Thanks\n\nRegards NestedForms.\nHappy Form Creating.")
        if value:
            cache.set(email,slug,timeout=300)
            return JsonResponse({'status':200,'message':'Password Recovery Instructions Send on Mail.'})
        else:
            return JsonResponse({'status':500,'message':'Err Human Validation Failed due to Empty Recaptcha Provided.'})
    except:
        return JsonResponse({'status':404,'message':'User Not Found.'})


def Renderresetpassword(request,email,token):
    try:
        ptoken = Fetch_cache(email)
        if str(ptoken).strip() == str(token).strip():
            return render(request,"changepass.html")
        return redirect('/')
    except:
        return redirect('/')



def ChangePass(request,email,token):
    if request.method == "POST":
        try:
            ptoken = Fetch_cache(email)
        except:
            return redirect('/')
        password = request.POST["pass"]
        cpassword = request.POST["cpass"]
        if password != cpassword:
            return redirect('/')
        if str(ptoken).strip() != str(token).strip():
            return redirect('/')
        status,msg = isValidPass(password,cpassword)
        if not status:
            return redirect('/')
        delete_pattern(email)
        user = User.objects.get(username=email)
        user.set_password(password)
        user.save()
        value = send_mail(to=email,subject="Password Changed! NestedForms.com",message=f"Your password Has been succesfully changed.")
        return redirect("/")
    return redirect('/')


def StrongPassOrNot(request):
    body = json.loads(request.body)
    pass1 = body.get("pass")
    pass2 = body.get("cpass")
    status,msg = isValidPass(pass1,pass2)
    if status:
        return JsonResponse({'status':200,'message':'success'})
    else:
        return JsonResponse({'status':406,'message':msg})


        # dummy account -> Hks@74123     ->   xyza@gmail.com