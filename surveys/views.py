from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from quizform.models import MCQTypeUserResponses, QuizMCQAnswers, QuizMCQquestions, QuizManager, base_submitted_form_data
import ast
from mainapp.models import formFillTypeQuestions, formFillTypeResponse, formMCQTypeResponse, formMCQquestions, formpublicdata,base_form_data_response
from django.http import JsonResponse
import json
from datetime import datetime
import pytz
from django.conf import settings

# Create your views here.

def RenderSurveyForQuiz(request,quiz_id):
    if not request.user.is_authenticated:
        return redirect('/login')
    try:
        code = QuizManager.objects.get(token=quiz_id)
    except:
        return render(request,'confirm.html',{'message':'Quiz Not Exists with provided id.'})
    mcqqus = QuizMCQquestions.objects.filter(code=code)
    rcode = base_submitted_form_data.objects.filter(token=quiz_id)
    if not len(rcode):
        return render(request,'confirm.html',{'message':'No Response exists to be analyse'})
    real_ans_objs = QuizMCQAnswers.objects.filter(code=code)
    final_data_Set = [[0,0,0,0] for i in range(len(real_ans_objs))]
    responses =  [0 for i in real_ans_objs]
    for codes in rcode:
        quizmodel = MCQTypeUserResponses.objects.filter(code=codes)
        cntr = 0
        res = 0
        for tindex,(model,rmodel) in enumerate(zip(quizmodel,real_ans_objs)):
            l1 = ast.literal_eval(model.answer)
            l2 = ast.literal_eval(rmodel.answers)
            if len(set(l1)) == 1 and l1[0] == '':
                pass
            else:
                responses[tindex] += 1
            if len(l1) != 1:
                for index,i in enumerate(l1):
                    if i != '':
                        final_data_Set[cntr][index] += 1
            else:
                if l1[0] != '':
                    if(mcqqus[tindex].option1) == l1[0]:
                        final_data_Set[cntr][0] += 1
                    elif(mcqqus[tindex].option2) == l1[0]:
                        final_data_Set[cntr][1] += 1
                    elif(mcqqus[tindex].option3) == l1[0]:
                        final_data_Set[cntr][2] += 1
                    elif(mcqqus[tindex].option4) == l1[0]:
                        final_data_Set[cntr][3] += 1
            cntr += 1
    render_this = []
    normal_list = []
    for sublist in final_data_Set:
        temp = []
        temp1 = []
        for index,value in enumerate(sublist):
            if index != 0:
                temp.append(round(temp[index-1]+(value/sum(sublist))*100,2))
            else:
                val = round((value/sum(sublist))*100,2)
                temp.append(val)
            temp1.append(round((value/sum(sublist))*100,2))
        render_this.append(temp)
        normal_list.append(temp1)

    questions = QuizMCQquestions.objects.filter(code=code)

    return render(request,'nf_survey.html',{'data':zip(render_this,questions,normal_list,responses),'additional':False})



def RenderSurveyForForm(request,form_id):
    if not request.user.is_authenticated:
        return redirect('/login')
    try:
        code = formpublicdata.objects.get(token=form_id)
    except:
        return render(request,'confirm.html',{'message':'Form Not Exists with provided id.'})

    rcode = base_form_data_response.objects.filter(token=form_id)
    
    if not len(rcode):
        return render(request,'confirm.html',{'message':'No Response exists to be analyse'})

    mcqqus = formMCQquestions.objects.filter(code=code)
    ftpqus = formFillTypeQuestions.objects.filter(code=code)

    
    final_data_Set = [[0,0,0,0] for i in range(len(mcqqus))]
    responses = [0 for i in mcqqus]
    for codes in rcode:
        quizmodel = formMCQTypeResponse.objects.filter(code=codes)
        cntr = 0
        for tindex,model in enumerate(quizmodel):
            l1 = ast.literal_eval(model.answer)
            if len(set(l1)) == 1 and l1[0] == '':
                pass
            else:
                responses[tindex] += 1
            # for managing radio
            if len(l1) != 1:
                for index,i in enumerate(l1):
                    if i != '':
                        final_data_Set[cntr][index] += 1
            else:
                if l1[0] != '':
                    if(mcqqus[tindex].option1) == l1[0]:
                        final_data_Set[cntr][0] += 1
                    elif(mcqqus[tindex].option2) == l1[0]:
                        final_data_Set[cntr][1] += 1
                    elif(mcqqus[tindex].option3) == l1[0]:
                        final_data_Set[cntr][2] += 1
                    elif(mcqqus[tindex].option4) == l1[0]:
                        final_data_Set[cntr][3] += 1
                
            cntr += 1

    render_this = []
    normal_list = []
    for sublist in final_data_Set:
        temp = []
        temp1 = []
        for index,value in enumerate(sublist):
            if index != 0:
                temp.append(round(temp[index-1]+(value/sum(sublist))*100,2))
            else:
                val = round((value/sum(sublist))*100,2)
                temp.append(val)
            temp1.append(round((value/sum(sublist))*100,2))
        render_this.append(temp)
        normal_list.append(temp1)
    
    # add ftp support here
    
    return render(request,'nf_survey.html',{'data':zip(render_this,mcqqus,normal_list,responses),'additional':True})


@csrf_exempt
def commonAPIsetNewOpenCloseTime(request):
    if request.method != "POST" or not request.user.is_authenticated:
        return JsonResponse({'status':400,'message':'Invalid Request.'})
    try:
        body = json.loads(request.body)
        quiz_id = body.get("quiz_id")
        form_id = body.get("form_id")
    except:
        return JsonResponse({'status':400,'message':'Invalid Request'})


    if quiz_id == None:
        # it's a form
        try:
            form = formpublicdata.objects.get(token=form_id)
        except:
            return JsonResponse({'status':404,'message':'form not found.'})
        if form.mail != request.user.email:
            return JsonResponse({'status':403,'message':'You need permission.'})
        
        try:
            open_at = body.get("open_at")
            open_till = body.get("close_at")
            timezone = body.get("timezone")
        except:
            return JsonResponse({'status':400,'message':'Invalid Request.'})

        if open_at!='' and open_till!='':
            try:
                date,time = open_at.split('T')
                year,month,day = date.split('-')
                hour,minute = time.split(':')
                date = f'{day}/{month}/{year} {hour}:{minute}:00'
                format  = "%d/%m/%Y %H:%M:%S"
                temp = datetime.strptime(date,format)
                local = pytz.timezone(timezone)
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
                form.open_at = open_at
                form.open_till = open_till
                form.save()
                return JsonResponse({'status':200,'message':'success'})
            except:
                return JsonResponse({'status':500,'message':'something went wrong.'})
        else:
            return JsonResponse({'status':406,'message':'blank informations.'})
    else:
        # it's a quiz
        try:
            quiz = QuizManager.objects.get(token=quiz_id)
        except:
            return JsonResponse({'status':404,'message':'quiz not found.'})
        if quiz.mail != request.user.email:
            return JsonResponse({'status':403,'message':'You need permission.'})
        try:
            open_at = body.get("open_at")
            open_till = body.get("close_at")
            timezone = body.get("timezone")
        except:
            return JsonResponse({'status':400,'message':'Invalid Request.'})
        if open_at!='' and open_till!='':
            try:
                date,time = open_at.split('T')
                year,month,day = date.split('-')
                hour,minute = time.split(':')
                date = f'{day}/{month}/{year} {hour}:{minute}:00'
                format  = "%d/%m/%Y %H:%M:%S"
                temp = datetime.strptime(date,format)
                local = pytz.timezone(timezone)
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
                quiz.open_at = open_at
                quiz.open_till = open_till
                quiz.save()
                return JsonResponse({'status':200,'message':'success'})
            except:
                return JsonResponse({'status':500,'message':'something went wrong.'})
        else:
            return JsonResponse({'status':406,'message':'blank informations.'})


def RenderUpdateTime(request,form_id):
    if not request.user.is_authenticated:
        return redirect('/login')
    try:
        form = formpublicdata.objects.get(token=form_id)
        if form.mail != request.user.email:
            return render(request,'confirm.html',{'message':'You have not sufficient permissions.'})
        return render(request,'changetime.html',{"id":form_id,"is_quiz":False,"timezones":settings.TIMEZONES})
    except:
        try:
            quiz = QuizManager.objects.get(token=form_id)
            if quiz.mail != request.user.email:
                return render(request,'confirm.html',{'message':'You have not sufficient permissions.'})
            return render(request,'changetime.html',{"id":form_id,"is_quiz":True,'timezones':settings.TIMEZONES})
        except:
            return render(request,'confirm.html',{'message':'Quiz or form not exist with provided informations.'})



def RenderDashboard(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    email = request.user.email
    forms = formpublicdata.objects.filter(mail=email)
    quizzes = QuizManager.objects.filter(mail=email)
    fids = []
    fnames = []
    fcd = []
    qids = []
    qnames = []
    qcd = []
    for form in forms:
        fids.append(form.token)
        fnames.append(form.title)
        fcd.append(form.date)
    for quiz in quizzes:
        qids.append(quiz.token)
        qnames.append(quiz.title)
        qcd.append(quiz.date)

    formdata = zip(fids,fnames,fcd)
    quizdata = zip(qids,qnames,qcd)
    
    return render(request,'commondashboard.html',{'formdata':formdata,'quizdata':quizdata,'lenform':len(fids),'lenquiz':len(qids)})