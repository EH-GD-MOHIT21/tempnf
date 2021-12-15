from django.http.response import Http404
from django.shortcuts import render,redirect
from numpy import fabs
from .models import formFillTypeQuestions, formFillTypeResponse, formMCQTypeResponse, formpublicdata,formMCQquestions,base_form_data_response as form_responses
from django.views.decorators.csrf import csrf_exempt
from random import choice,randint
from datetime import datetime
import ast
from django.http import JsonResponse
import json
from django.utils import timezone
import pytz
from django.conf import settings

# Create your views here.


def home(request):
    return render(request,'home.html')


def saveresponse(request,formid=None):
    if not request.user.is_authenticated:
        return render(request,'confirm.html',{'message':'Please Login to fill a form.'})
    if request.method != "POST":
        return redirect('/')
    try:
        myformdata = formpublicdata.objects.get(token=formid)
    except:
        return render(request,'confirm.html',{'message':"Required Form Doesn't Exists."})
    try:
        form_responses.objects.get(token=formid,email=request.user.email)
        return render(request,'confirm.html',{'message':"You've already responded"})
    except Exception as e:
        pass

    if myformdata.open_at != None and myformdata.open_till != None:

        if not (timezone.now() >= myformdata.open_at and timezone.now() <= myformdata.open_till):
            return render(request,'confirm.html',{'message':f'Server Time for fill the form is between {myformdata.open_at} and {myformdata.open_till}. Your Responses can not be save.'})

    elif not myformdata.accept_response:
        return render(request,'confirm.html',{'message':'This Form is no longer accepting response.'})

    name = request.POST['name']
    mail = request.user.email
    phone = request.POST['phone']
    address = request.POST['address']

    mcqans = []
    ftpans = []
    i = 0
    while True:
        try:
            request.POST["mcq-"+str(i)]
        except Exception as e:
            print(e)
            break
        data = request.POST.getlist("mcq-"+str(i))
        mcqans.append(data)
        i+=1

    i = 0
    while True:
        try:
            request.POST["ftp-"+str(i)]
        except Exception as e:
            print(e)
            break
        data = request.POST.getlist("ftp-"+str(i))
        ftpans.append(data)
        i+=1
    
    # final db work here

    #base model creation
    model = form_responses()
    model.token = formid
    model.name = name
    model.email = mail
    model.phone_no = phone
    model.address = address
    model.save()

    # mcq type user response model
    for ans in mcqans:
        tmodel = formMCQTypeResponse()
        tmodel.code = model
        tmodel.answer = ans
        tmodel.save()

    # fill type ans saver

    for ans in ftpans:
        tmodel = formFillTypeResponse()
        tmodel.code = model
        tmodel.answer = str(ans[0])
        tmodel.save()

        

    return render(request,'confirm.html',{'message':'Your Responses have been successfully submitted.'})



def fillform(request,formid=None):
    if not request.user.is_authenticated:
        return redirect('/login')
    if formid == None:
        return redirect('/login')
    try:
        form_responses.objects.get(token=formid,email=request.user.email)
        return render(request,'confirm.html',{'message':"You've Already Responded."})
    except:
        pass
    try:
        myformdata = formpublicdata.objects.get(token=formid)
        element = myformdata
    except:
        return render(request,'confirm.html',{'message':"Required Form Not Exists"})

    # if not myformdata.accept_response:
    #     return render(request,'confirm.html',{'message':'This Form is no longer accepting response.'})


    if myformdata.open_at != None and myformdata.open_till != None:

        if not (timezone.now() >= myformdata.open_at and timezone.now() <= myformdata.open_till):
            return render(request,'confirm.html',{'message':f'Server Time for fill the form is between {myformdata.open_at} and {myformdata.open_till}'})

    elif not myformdata.accept_response:
        return render(request,'confirm.html',{'message':'This Form is no longer accepting response.'})
    
    fmcq = formMCQquestions.objects.filter(code=myformdata)
    ftpq = formFillTypeQuestions.objects.filter(code=myformdata)
    questions = []
    option1 = []
    option2 = []
    option3 = []
    option4 = []
    ftpqus = []
    is_multi = []
    for mcqs in fmcq:
        questions.append(mcqs.question)
        option1.append(mcqs.option1)
        option2.append(mcqs.option2)
        option3.append(mcqs.option3)
        option4.append(mcqs.option4)
        is_multi.append(mcqs.is_multi_correct)
    main_list = zip(questions,option1,option2,option3,option4,is_multi)
    content = {
        'mainlist':main_list
    }
    try:
        del_time = myformdata.open_till-timezone.now()
        hours,minutes,seconds = map(float,str(del_time).split(':'))
        total_seconds = hours*60*60 + minutes*60 + seconds
    except:
        total_seconds = 0
    for qus in ftpq:
        ftpqus.append(qus.question)
    return render(request,'quiz.html',{'title':element.title,'desc':element.desc,'creator':element.creator,'mail':element.mail,'content':content,'formid':formid,'filltype':ftpqus,'opentill':int(total_seconds)})



def createform(request):
    if request.user.is_authenticated:
        return render(request,'index.html',{'timezones':settings.TIMEZONES})
    else:
        return redirect('/login')



def generateaunicode():
    varsptoken = ''
    alphas = ['-','_','0','1','2','3','4','5','6','7','8','9']
    for i in range(26):
        alphas.append(chr(65+i))
        alphas.append(chr(97+i))
    for i in range(randint(30,60)):
        varsptoken += choice(alphas)
    time_now = str(datetime.now())
    dels = [' ','-',':','.']
    for d in dels:
        time_now = time_now.replace(d,'_')
    
    varsptoken += time_now
    return (varsptoken)



@csrf_exempt
def savedetails(request):
    if not request.user.is_authenticated:
        return render(request,'confirm.html',{'message':'Please Login And Try Again.'})
    if not request.method == "POST":
        return redirect('/')

    personalcode = generateaunicode()
    
    title = request.POST['formtitle']
    mail = request.user.email
    creatorname = request.POST['creatorname']
    desc = request.POST['formdesc']

    open_at = request.POST['opentime']
    open_till = request.POST['closetime']
    print(open_at)

    model = formpublicdata()
    model.token = personalcode
    model.title = title
    model.mail = mail
    model.creator = creatorname
    model.desc = desc
    model.set_date
    if open_at!='' and open_till!='':
        try:
            date,time = open_at.split('T')
            year,month,day = date.split('-')
            hour,minute = time.split(':')
            date = f'{day}/{month}/{year} {hour}:{minute}:00'
            format  = "%d/%m/%Y %H:%M:%S"
            print(request.POST["timezone"])
            local = pytz.timezone(request.POST["timezone"])
            temp = datetime.strptime(date,format)
            local_dt = local.localize(temp, is_dst=None)
            temp = local_dt.astimezone(pytz.UTC)
            open_at = temp
            date,time = open_till.split('T')
            year,month,day = date.split('-')
            hour,minute = time.split(':')
            date = f'{day}/{month}/{year} {hour}:{minute}:00'
            format  = "%d/%m/%Y %H:%M:%S"
            temp = datetime.strptime(date,format)
            local_dt = local.localize(temp, is_dst=None)
            temp = local_dt.astimezone(pytz.UTC)
            open_till = temp
            print(open_at)
            print(open_till)
            model.open_at = open_at
            model.open_till = open_till
        except Exception as e:
            pass
    model.save()

    mcqqus = request.POST.getlist("questionmcq")
    option1 = request.POST.getlist("option1")
    option2 = request.POST.getlist("option2")
    option3 = request.POST.getlist("option3")
    option4 = request.POST.getlist("option4")
    multicorrect = request.POST.getlist("multicorrect")

    for qus,opt1,opt2,opt3,opt4,ismc in zip(mcqqus,option1,option2,option3,option4,multicorrect):
        tmodel = formMCQquestions()
        tmodel.code = model
        tmodel.question = qus
        tmodel.option1 = opt1
        tmodel.option2 = opt2
        tmodel.option3 = opt3
        tmodel.option4 = opt4
        if ismc.strip() == "1":
            tmodel.is_multi_correct = True
        else:
            tmodel.is_multi_correct = False
        tmodel.save()

    ftpqus = request.POST.getlist("questionftp")
    for qus in ftpqus:
        tmodel = formFillTypeQuestions()
        tmodel.code = model
        tmodel.question = qus
        tmodel.save()
    return render(request,'logshower.html',{'formid':personalcode,'message':'success'})
    

@csrf_exempt
def getformbyid(request):
    # need tobe rewrite
    formid = request.POST['formtoken']
    myformdata = formpublicdata.objects.filter(code=formid)
    if len(myformdata)==1:
        for element in myformdata:
            fmcq = formMCQquestions.objects.filter(code=formid)
            questions = []
            option1 = []
            option2 = []
            option3 = []
            option4 = []
            for mcqs in fmcq:
                questions.append(mcqs.question)
                option1.append(mcqs.option1)
                option2.append(mcqs.option2)
                option3.append(mcqs.option3)
                option4.append(mcqs.option4)
            main_list = zip(questions,option1,option2,option3,option4)
            content = {
                'mainlist':main_list
            }
            return render(request,'quiz.html',{'title':element.title,'desc':element.desc,'creator':element.creator,'mail':element.mail,'content':content,'formid':formid})
    else:
        return render(request,'confirm.html',{'special':'yes'})




def fillformuser(request):
    if request.user.is_authenticated:
        return render(request,'confirm.html',{'special':'yes'})
    else:
        return redirect('/login')



def showresponsepage(request,formid=None,email=None):
    if not request.user.is_authenticated:
        return render(request,'confirm.html',{'message':'Please Login to authenticate.'})
    try:
        form = formpublicdata.objects.get(token=formid)
    except:
        return render(request,'confirm.html',{'message':'Invalid Form Id.'})

    if not form.show_response and not request.user.is_superuser and request.user.email != form.mail:
        return render(request,'confirm.html',{'message':'You Need Permission.'})

    try:
        email = request.GET["email"]
        
        title = form.title
        desc = form.desc
        author = form.creator
        contact = form.mail
        responses_obj = form_responses.objects.get(token=formid,email=email)
        
        fmcqs = formMCQquestions.objects.filter(code=form)
        questions = []
        option1 = []
        option2 = []
        option3 = []
        option4 = []
        is_multi_correct = []
        for mcq in fmcqs:
            questions.append(mcq.question)
            option1.append(mcq.option1)
            option2.append(mcq.option2)
            option3.append(mcq.option3)
            option4.append(mcq.option4)
            is_multi_correct.append(mcq.is_multi_correct)
        responses = []
        resps = formMCQTypeResponse.objects.filter(code=responses_obj)
        for res in resps:
            responses.append(ast.literal_eval(res.answer))
        ftpresp = formFillTypeResponse.objects.filter(code=responses_obj)
        ftpqus = []
        ftpresponses = []
        ffilltpsq = formFillTypeQuestions.objects.filter(code=form)
        for qus in ffilltpsq:
            ftpqus.append(qus.question)
        for ans in ftpresp:
            ftpresponses.append(str(ans.answer))
        print(ftpqus,ftpresponses)
        # fetch responses from db --> pending
        data = zip(questions,option1,option2,option3,option4,responses,is_multi_correct)
        # pick qus from formpublic data
        username = responses_obj.name
        mail = responses_obj.email
        phone = responses_obj.phone_no
        address = responses_obj.address

        ftpdata = zip(ftpqus,ftpresponses)
        
        # permission <<<->>>

        if (email == request.user.email) or (form.mail==request.user.email) or (request.user.is_superuser):
            return render(request,'showresponses.html',{'title':title,'desc':desc,'author':author,'contact':contact,'data':data,'username':username,'mail':mail,'phone':phone,'address':address,'ftpdata':ftpdata})
        
        return render(request,'confirm.html',{'message':'You Cannot see someone others responses.'})

    except Exception as e:
        # raise(e)
        print(e)
        return redirect('/')
    
    

def creatorpageview(request):
    if request.user.is_authenticated:
        forms = formpublicdata.objects.filter(mail=request.user.email)
        formids = []
        view_perms = []
        fill_perms = []
        is_sch = []
        open_at = []
        open_till = []
        for form in forms:
            formids.append(form.token)
            view_perms.append(form.show_response)
            if type(form.open_at)==type(timezone.now()) and type(form.open_till)==type(timezone.now()):
                if timezone.now() >= form.open_at and timezone.now() <= form.open_till:
                    fill_perms.append(True)
                    if not form.accept_response:
                        form.accept_response = True
                        form.save()
                else:
                    form.accept_response = False
                    form.save()
                    fill_perms.append(False)
                is_sch.append(True)
            else:
                fill_perms.append(form.accept_response)
                is_sch.append(False)
            open_at.append(form.open_at)
            open_till.append(form.open_till)
        total_res = []
        responses = []
        
        for ids in formids:
            temp = []
            data = form_responses.objects.filter(token=ids)
            for dat in data:
                temp.append(dat.email)
            responses.append(temp)
            total_res.append(len(data))
        data = zip(formids,total_res,view_perms,fill_perms,is_sch,open_at,open_till)
        # print(responses)
        for form in forms:
            return render(request,'creator.html',{'data':data,'mail':request.user.email,'resdata':responses})
        return render(request,'confirm.html',{'message':'You Have Not created Any forms please create some.'})
    else:
        return redirect('/login')


@csrf_exempt
def set_form_res_visibility_Api(request):
    if not request.user.is_authenticated or not request.method == "POST":
        return JsonResponse({'status':400,'message':'Invalid Request.'})
    body = json.loads(request.body)
    form_id = body.get("form_id")
    try:
        form = formpublicdata.objects.get(token=form_id)
        if form.show_response:
            form.show_response = False
        else:
            form.show_response = True
        form.save()
        return JsonResponse({'status':200,'message':'success'})
    except:
        return JsonResponse({'status':404,'message':'Invalid form Id.'})


@csrf_exempt
def delete_form_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status':403,'message':'User Not authenticated.'})
    body = json.loads(request.body)
    form_id = body.get("form_id")
    email = body.get("email")

    try:
        formpublicdata.objects.get(token=form_id,mail=email).delete()
    except:
        return JsonResponse({'status':406,'message':'Quiz Doesnot exists or you donot have permission to delete quiz.'})

    try:
        # do ssame in quiz delete 
        forms = form_responses.objects.filter(token=form_id)
        for form in forms:
            form.delete()
    except:
        pass

    return JsonResponse({'status':200,'message':'success'})

    # complete it.

@csrf_exempt
def delete_form_response_api(request):
    if not request.user.is_authenticated or not request.method=="POST":
        return JsonResponse({'status':400,'message':'Invalid Request.'})
    body = json.loads(request.body)
    form_id = body.get("form_id")
    email_del_res = body.get("email")
    try:
        formpublicdata.objects.get(token=form_id,mail=request.user.email)
    except:
        return JsonResponse({'status':404,'message':'quiz not found.'})
    try:
        user_res = form_responses.objects.get(token=form_id,email=email_del_res)
        user_res.delete()
        return JsonResponse({'status':200,'message':'success'})
    except:
        return JsonResponse({'status':404,'message':'User response not exists.'})


@csrf_exempt
def set_form_acpres_Api(request):
    if not request.user.is_authenticated or not request.method == "POST":
        return JsonResponse({'status':400,'message':'Invalid Request.'})
    body = json.loads(request.body)
    form_id = body.get("form_id")
    try:
        form = formpublicdata.objects.get(token=form_id)
        if type(form.open_at)==type(timezone.now()) and type(form.open_till)==type(timezone.now()):
            if form.open_till < timezone.now():
                return JsonResponse({'status':200,'message':'Please Change Schedule of quiz to continue accepting response.'})
            else:
                return JsonResponse({'status':200,'message':'This Quiz is a schedule quiz please change schedule to stop receiving response.'})
        if form.accept_response:
            form.accept_response = False
        else:
            form.accept_response = True
        form.save()
        return JsonResponse({'status':200,'message':'success'})
    except:
        return JsonResponse({'status':404,'message':'Invalid form Id.'})



def handler_404(request, exception=None):
    '''
        view to handle 404 error
        attached in project level
        urls.py (gform.urls)
    '''
    data = {}
    return render(request,'404error.html', data)


def handler_500(request,  exception=None):
    '''
        view to handle 500 error
        attached in project level
        urls.py (gform.urls)
    '''
    data = {}
    return render(request,'500error.html', data)