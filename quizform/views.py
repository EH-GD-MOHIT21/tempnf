from django.db.models import base
from django.shortcuts import redirect, render
from django.views.decorators import csrf
from .app_utils.model_manager import *
from .models import *
import ast
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Create your views here.

def RenderCreateQuiz(request):
    if request.user.is_authenticated:
        return render(request,'createquiz.html',{'timezones':settings.TIMEZONES})
    else:
        return redirect('/login')


def SaveQuiz(request):
    if request.method == "POST" and request.user.is_authenticated:
        marks = request.POST.getlist("markmcq")
        for mark in marks:
            try:
                mark = float(mark)
                if mark < 0 or mark > 1000:
                    return render(request,'confirm.html',{'message':'Invalid marks provided.'})
            except:
                return render(request,'confirm.html',{'message':'Invalid marks provided.'})
        token,model = QuizManagerObjectCreator(request)
        MCQTypeQuestionSaver(request,model)
        FillTypeQuestionSaver(request,model)
        # ans of quizes may be empty
        MCQTypeAnswerSaver(request,model)
        print(token)
        return render(request,'logshower.html',{'quizid':token,'quiz':True})
    else:
        return redirect('/login')


def FillQuiz(request,quiz_id):
    if not request.user.is_authenticated:
        return redirect('/login')

    try:
        base_submitted_form_data.objects.get(token=quiz_id,email=request.user.email)
        return render(request,'confirm.html',{'message':'You have already responded.'})
    except:
        pass

    try:
        model = QuizManager.objects.get(token=quiz_id)
        if model.open_at != None and model.open_till != None:
            if not (timezone.now() >= model.open_at and timezone.now() <= model.open_till):
                return render(request,'confirm.html',{'message':f'Server Time for fill the quiz is between {model.open_at} and {model.open_till}'})

        elif not model.accept_response:
            return render(request,'confirm.html',{'message':'This quiz is no longer accepting responses.'})
        mcqques = QuizMCQquestions.objects.filter(code=model)
        filltype = QuizFillTypeQuestions.objects.filter(code=model)
        answers = QuizMCQAnswers.objects.filter(code=model)
        title = model.title
        mail = model.mail
        creator_name = model.creator.first_name + " " + model.creator.last_name
        desc = model.desc
        mcqquestions = []
        marksmcq = []
        marksfilltype = []
        option1 = []
        option2 = []
        option3 = []
        option4 = []
        fillques = []
        is_single = []
        for questions in mcqques:
            mcqquestions.append(questions.question)
            option1.append(questions.option1)
            option2.append(questions.option2)
            option3.append(questions.option3)
            option4.append(questions.option4)
            marksmcq.append(questions.marks)

        for ans in answers:
            a = [ans.option1,ans.option2,ans.option3,ans.option4]
            if a.count(True)==1:
                is_single.append(True)
            else:
                is_single.append(False)
    
            
        for questions in filltype:
            fillques.append(questions.question)
            marksfilltype.append(questions.marks)

        total_marks = sum(marksmcq)+sum(marksfilltype)

        mcqs = zip(mcqquestions,option1,option2,option3,option4,is_single,marksmcq)
        upper = {
            "title":title,
            "mail":mail,
            "creator":creator_name,
            "desc":desc,
            "cur_user":request.user.email,
            "total_marks":total_marks,
        }

        try:
            del_time = model.open_till-timezone.now()
            hours,minutes,seconds = map(float,str(del_time).split(':'))
            total_seconds = hours*60*60 + minutes*60 + seconds
        except:
            total_seconds = 0
            

        return render(request,'fillquiz.html',{
            "upper":upper,
            "mcqs":mcqs,
            "filltype": zip(fillques,marksfilltype),
            "opentill":int(total_seconds)
        })
    except Exception as e:
        return render(request,'quiz_confirmation.html',{"message":"Quiz Not Found With Provided Token"})



def SaveQuizResposnes(request,quiz_id):
    if not request.user.is_authenticated or request.method != "POST":
        return redirect('/login')
    try:
        code = QuizManager.objects.get(token=quiz_id)
        neg_markinng = code.negative_marking_scheme
    except:
        return render(request,'quiz_confirmation.html',{"message":"Quiz Not Found With Provided Token"})

    if code.open_at != None and code.open_till != None:

        if not (timezone.now() >= code.open_at and timezone.now() <= code.open_till):
            return render(request,'confirm.html',{'message':f'Server Time for fill the quiz is between {code.open_at} and {code.open_till}. Your Responses can not be save.'})
    
    elif not code.accept_response:
            return render(request,'confirm.html',{'message':'This quiz is no longer accepting response.'})

    # fill type answers
    try:
        base_submitted_form_data.objects.get(token=quiz_id,email=request.user.email)
        return render(request,'confirm.html',{'message':'You have already responded.'})
        # show you have already responded
    except:
        pass

    marks = []
    for elm in QuizMCQquestions.objects.filter(code=code):
        marks.append(elm.marks)

    print(marks)
        
    model = base_submitted_form_data()
    model.token = quiz_id
    model.name = request.POST["name"]
    model.email = request.user.email
    model.phone_no = request.POST["phone"]
    model.address = request.POST["address"]
    model.save()
    i = 0
    while True:
        try:
            data = request.POST["ftp-"+str(i)]
            ftpuser = FillTypeUserResponses()
            ftpuser.code = model
            ftpuser.answer = data
            ftpuser.save()
            i+=1
        except:
            break

    j = 0
    while True:
        try:
            request.POST["i-"+str(j)]
            option = request.POST.getlist("i-"+str(j))
            mcqtype = MCQTypeUserResponses()
            mcqtype.code = model
            mcqtype.answer = option
            # check here mcq type qus
            real_ans = ast.literal_eval(QuizMCQAnswers.objects.filter(code=code)[j].answers)
            mark = 0
            print(option,real_ans)
            if neg_markinng == None or neg_markinng == '':
                for value in option:
                    if value in real_ans and value != '':
                        mark += (marks[j]/len(real_ans))
                    elif value != '' and value not in real_ans:
                        # mark -= (marks[j]/3)
                        mark = 0
                        break
                mcqtype.final_marks = max(0,mark)
            else:
                for value in option:
                    if value in real_ans and value != '':
                        mark += (marks[j]/len(real_ans))
                    elif value != '' and value not in real_ans:
                        mark -= (marks[j]*neg_markinng)
                mcqtype.final_marks = mark
            mcqtype.save()
            j+=1
        except Exception as e:
            print(e)
            break

    return render(request,'confirm.html')



def ManageQuizes(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    quizzes_codes = []
    all_quizes = QuizManager.objects.filter(mail=request.user.email)
    permissions = []
    accepting = []
    is_sch = []
    open_at = []
    open_till = []
    dates = []
    for quiz in all_quizes:
        quizzes_codes.append(quiz.token)
        permissions.append(quiz.show_response)
        dates.append(quiz.date)
        if type(quiz.open_at)==type(timezone.now()) and type(quiz.open_till)==type(timezone.now()):
            if timezone.now() >= quiz.open_at and timezone.now() <= quiz.open_till:
                accepting.append(True)
                if not quiz.accept_response:
                    quiz.accept_response = True
                    quiz.save()
            else:
                quiz.accept_response = False
                quiz.save()
                accepting.append(False)
            is_sch.append(True)
        else:
            accepting.append(quiz.accept_response)
            is_sch.append(False)
        open_at.append(quiz.open_at)
        open_till.append(quiz.open_till)
    
    total_res = []
    responses = []
    for ids in quizzes_codes:
        temp = []
        data = base_submitted_form_data.objects.filter(token=ids)
        for dat in data:
            temp.append(dat.email)
        responses.append(temp)
        total_res.append(len(data))
    data = zip(quizzes_codes,total_res,permissions,accepting,is_sch,open_at,open_till,dates)

    for quiz in quizzes_codes:
        return render(request,'managequizes.html',{'data':data,'mail':request.user.username,'resdata':responses})
    return render(request,'confirm.html',{'message':'You Have Not created Any Quizzes please create some.'})
    



def showresponses(request,quiz_id):
    if not request.user.is_authenticated:
        return render(request,'confirm.html',{'message':'Please Login to authenticate.'})

    try:
        email = request.GET["email"]
        quiz = QuizManager.objects.get(token=quiz_id)
        if not quiz.show_response and not request.user.is_superuser and request.user.email != quiz.mail:
            return render(request,'confirm.html',{'message':'You need permissions.'})
        title = quiz.title
        desc = quiz.desc
        author = quiz.creator.first_name + " " + quiz.creator.last_name
        contact = quiz.mail
        date = quiz.date

        responses_obj = base_submitted_form_data.objects.get(token=quiz_id,email=email)
        fmcqs = QuizMCQquestions.objects.filter(code=quiz)
        filltypequs = QuizFillTypeQuestions.objects.filter(code=quiz)

        fqus = []
        fmarks = []
        for qus in filltypequs:
            fqus.append(qus.question)
            fmarks.append(qus.marks)
        questions = []
        option1 = []
        option2 = []
        option3 = []
        option4 = []
        marks = []
        for mcq in fmcqs:
            questions.append(mcq.question)
            option1.append(mcq.option1)
            option2.append(mcq.option2)
            option3.append(mcq.option3)
            option4.append(mcq.option4)
            marks.append(mcq.marks)
        # pick qus from formpublic data
        username = responses_obj.name
        mail = responses_obj.email
        phone = responses_obj.phone_no
        address = responses_obj.address
        filltype = []

        filltypesubmitted = FillTypeUserResponses.objects.filter(code=responses_obj)
        filltypeusermarks = []
        for obj in filltypesubmitted:
            filltype.append(obj.answer)
            filltypeusermarks.append(obj.final_marks)
    
        mcqtypesubmitted = MCQTypeUserResponses.objects.filter(code=responses_obj)
        real_ans = QuizMCQAnswers.objects.filter(code=quiz)

        gained_marks = []

        mymcqans = []
        rightmcqans = []
        
        for index,obj in enumerate(mcqtypesubmitted):
            userfilled = ast.literal_eval(obj.answer)
            right_ans = ast.literal_eval(real_ans[index].answers)
            mymcqans.append(userfilled)
            rightmcqans.append(right_ans)
            gained_marks.append(obj.final_marks)

        
        total_valid_ftpemarks = sum(fmarks)
        total_earned_ftypemarks = sum(filltypeusermarks)
        total_valid_mcqmarks = sum(marks)
        total_earned_mcqmarks = sum(gained_marks)

        totalmarks = total_valid_mcqmarks + total_valid_ftpemarks
        totalearned = total_earned_mcqmarks + total_earned_ftypemarks

        fdata = zip(fqus,filltype,fmarks,filltypeusermarks)
        data = zip(questions,option1,option2,option3,option4,mymcqans,rightmcqans,gained_marks,marks)

        # permission <<<->>>

        if (email == request.user.username) or (quiz.mail==request.user.username) or (request.user.is_superuser):
            return render(request,'quizresponse.html',{'title':title,'desc':desc,'author':author,'contact':contact,'data':data,'username':username,'mail':mail,'phone':phone,'address':address,'date':date,'fdata':fdata,'totalmarks':totalmarks,'totalearned':totalearned})
        
        return render(request,'confirm.html',{'message':'You Cannot see someone others responses.'})

    except Exception as e:
        print(e)
        return redirect('/')


@csrf_exempt
def update_mark_filltype_Api(request):
    body = json.loads(request.body)

    if not request.user.is_authenticated:
        return JsonResponse({'status':403,'message':'User Not authenticated'})

    quiz_id = body.get("quiz_id")
    qus_id = body.get("qus_id")
    marks = body.get("marks")
    usermail = body.get("usermail")
    email = request.user.email

    try:
        marks = float(marks)
    except:
        return JsonResponse({'status':400,'message':'Invalid Value for marks.'})

    if marks == None or marks == '' or marks < 0 or marks > 1000:
        return JsonResponse({'status':406,"message":"marks can be between 0-1000 "})

    try:
        quizmanager = QuizManager.objects.get(token=quiz_id)
        if quizmanager.mail != email:
            return JsonResponse({'status':400,'message':'You do not have permissions to change marks.'})
        quizqus = QuizFillTypeQuestions.objects.filter(code=quizmanager).order_by("id")
        
        base_form = base_submitted_form_data.objects.get(token=quiz_id,email=usermail)
        ftresponse = FillTypeUserResponses.objects.filter(code=base_form).order_by("id")
        finalchangeablemodel = ftresponse[int((qus_id).split('-')[1])]
        print(finalchangeablemodel)
        max_marks = quizqus[int((qus_id).split('-')[1])].marks

        if float(marks) <= float(max_marks):
            finalchangeablemodel.final_marks = marks
            finalchangeablemodel.save()
            return JsonResponse({'status':200,'message':'success'})
        
        return JsonResponse({'status':400,'message':'max marks can not be less than provided.'})
        # get_marks = 
    except Exception as e:
        print(e)
        return JsonResponse({'status':400,'message':'No quiz or response exists with provided details.'})


@csrf_exempt
def delete_quiz_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status':403,'message':'User Not authenticated.'})
    body = json.loads(request.body)
    quiz_id = body.get("quiz_id")
    email = body.get("email")

    try:
        QuizManager.objects.get(token=quiz_id,mail=email).delete()
    except:
        return JsonResponse({'status':406,'message':'Quiz Doesnot exists or you donot have permission to delete quiz.'})

    try:
        base_submitted_form_data.objects.get(token=quiz_id,email=email).delete()
    except:
        pass

    return JsonResponse({'status':200,'message':'success'})

    # complete it.

@csrf_exempt
def delete_response_api(request):
    if not request.user.is_authenticated or not request.method=="POST":
        return JsonResponse({'status':400,'message':'Invalid Request.'})
    body = json.loads(request.body)
    quiz_id = body.get("quiz_id")
    email_del_res = body.get("email")
    try:
        QuizManager.objects.get(token=quiz_id,mail=request.user.email)
    except:
        return JsonResponse({'status':404,'message':'quiz not found.'})
    try:
        user_res = base_submitted_form_data.objects.get(token=quiz_id,email=email_del_res)
        user_res.delete()
        return JsonResponse({'status':200,'message':'success'})
    except:
        return JsonResponse({'status':404,'message':'User response not exists.'})


@csrf_exempt
def set_quiz_res_visibility_Api(request):
    if not request.user.is_authenticated or not request.method == "POST":
        return JsonResponse({'status':400,'message':'Invalid Request.'})
    body = json.loads(request.body)
    quiz_id = body.get("quiz_id")
    try:
        quiz = QuizManager.objects.get(token=quiz_id,mail=request.user.email)
        if quiz.show_response:
            quiz.show_response = False
        else:
            quiz.show_response = True
        quiz.save()
        return JsonResponse({'status':200,'message':'success'})
    except:
        return JsonResponse({'status':404,'message':'Invalid Quiz Id.'})


@csrf_exempt
def set_accepting_respquiz_api(request):
    if not request.user.is_authenticated or not request.method == "POST":
        return JsonResponse({'status':400,'message':'Invalid Request.'})
    body = json.loads(request.body)
    quiz_id = body.get("quiz_id")
    try:
        quiz = QuizManager.objects.get(token=quiz_id,mail=request.user.email)
        if type(quiz.open_at)==type(timezone.now()) and type(quiz.open_till)==type(timezone.now()):
            if quiz.open_till < timezone.now():
                return JsonResponse({'status':200,'message':'Please Change Schedule of quiz to continue accepting response.'})
            else:
                return JsonResponse({'status':200,'message':'This Quiz is a schedule quiz please change schedule to stop receiving response.'})
        if quiz.accept_response:
            quiz.accept_response = False
        else:
            quiz.accept_response = True
        quiz.save()
        return JsonResponse({'status':200,'message':'success'})
    except:
        return JsonResponse({'status':404,'message':'Invalid Quiz Id.'})


def ExpendResponseQuiz(request,quiz_id):
    try:
        quiz = QuizManager.objects.get(token=quiz_id)
        if not request.user.is_authenticated or quiz.mail != request.user.email:
            return redirect('/login')
        return render(request,'manage_responses.html',{'is_quiz':True})
    except:
        return render(request,'confirm.html',{'message':'Quiz Not Exists.'})


@csrf_exempt
def SendQuizResData(request,quiz_id):
    
    if not request.method == "POST" or not request.user.is_authenticated:
        return JsonResponse({'status':406,'message':'Invalid Request','data':None})

    try:
        body = json.loads(request.body)
        filters = body.get("filters")
    except:
        pass

    try:
        quiz = QuizManager.objects.get(token=quiz_id)
        title = quiz.title
        creator = quiz.creator.first_name + " " +quiz.creator.last_name
        desc = quiz.desc
        date = quiz.date
        if quiz.mail != request.user.email:
            return JsonResponse({'status':403,'message':'You need permissions','data':None})
        if filters == None:
            resp = base_submitted_form_data.objects.filter(token=quiz_id)
        else:
            if filters == "Time":
                resp = base_submitted_form_data.objects.filter(token=quiz_id)
            elif filters == "Name":
                resp = base_submitted_form_data.objects.filter(token=quiz_id).order_by("name")
            elif filters == "Phone":
                resp = base_submitted_form_data.objects.filter(token=quiz_id).order_by("phone_no")
            elif filters == "Email":
                resp = base_submitted_form_data.objects.filter(token=quiz_id).order_by("email")
            elif filters == "Address":
                resp = base_submitted_form_data.objects.filter(token=quiz_id).order_by("address")
    except:
        return JsonResponse({'status':404,'message':'quiz not exists','data':None})
    
    if not len(resp):
        return JsonResponse({'status':200,'message':'success','data':None,'extdata':{
        "title": title,
        "creator": creator,
        "date": date,
        "desc": desc
    }
    })
    names = []
    emails = []
    phone_no = []
    address = []
    for res in resp:
        names.append(res.name)
        emails.append(res.email)
        phone_no.append(res.phone_no)
        address.append(res.address)
    data = {
        "names":names,
        "emails":emails,
        "phone_no": phone_no,
        "address": address,
    }
    
    return JsonResponse({'status':200,'message':'success','data':data,'extdata':{"title": title,
        "creator": creator,
        "date": date,
        "desc": desc
    }
    })