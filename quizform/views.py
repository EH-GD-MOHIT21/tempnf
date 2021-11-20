from django.db.models import base
from django.shortcuts import redirect, render
from .app_utils.model_manager import *
from .models import *
import ast
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def RenderCreateQuiz(request):
    if request.user.is_authenticated:
        return render(request,'createquiz.html')
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
            

        return render(request,'fillquiz.html',{
            "upper":upper,
            "mcqs":mcqs,
            "filltype": zip(fillques,marksfilltype)
        })
    except Exception as e:
        return render(request,'quiz_confirmation.html',{"message":"Quiz Not Found With Provided Token"})



def SaveQuizResposnes(request,quiz_id):
    if not request.user.is_authenticated or request.method != "POST":
        return redirect('/login')
    try:
        code = QuizManager.objects.get(token=quiz_id)
    except:
        return render(request,'quiz_confirmation.html',{"message":"Quiz Not Found With Provided Token"})
    # fill type answers
    try:
        base_submitted_form_data.objects.get(token=quiz_id,email=request.user.email)
        return render(request,'confirm.html',{'message':'You have already responded.'})
        # show you have already responded
    except:
        pass
        
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
            mcqtype.save()
            j+=1
        except:
            break

    return redirect('/')



def ManageQuizes(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    quizzes_codes = []
    all_quizes = QuizManager.objects.filter(mail=request.user.email)
    for quiz in all_quizes:
        quizzes_codes.append(quiz.token)
    
    total_res = []
    responses = []
    for ids in quizzes_codes:
        temp = []
        data = base_submitted_form_data.objects.filter(token=ids)
        for dat in data:
            temp.append(dat.email)
        responses.append(temp)
        total_res.append(len(data))
    data = zip(quizzes_codes,total_res)

    for form in quizzes_codes:
        return render(request,'managequizes.html',{'data':data,'mail':request.user.username,'resdata':responses})
    return render(request,'confirm.html',{'message':'You Have Not created Any Quizzes please create some.'})
    



def showresponses(request,quiz_id):
    if not request.user.is_authenticated:
        return render(request,'confirm.html',{'message':'Please Login to authenticate.'})

    try:
        email = request.GET["email"]
        quiz = QuizManager.objects.get(token=quiz_id)
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
            mark = 0
            userfilled = ast.literal_eval(obj.answer)
            right_ans = ast.literal_eval(real_ans[index].answers)
            
            mymcqans.append(userfilled)
            rightmcqans.append(right_ans)

            for value in userfilled:
                if value in right_ans and value != '':
                    mark += (marks[index]/len(right_ans))

            gained_marks.append(mark)

        
        total_valid_ftpemarks = sum(fmarks)
        total_earned_ftypemarks = sum(filltypeusermarks)
        total_valid_mcqmarks = sum(marks)
        total_earned_mcqmarks = sum(gained_marks)

        totalmarks = total_valid_mcqmarks + total_valid_ftpemarks
        totalearned = total_earned_mcqmarks + total_earned_ftypemarks
        
        # permission <<<->>>

        '''
        questions,option1-4
        mymcqans,rightmcqans,gained_marks,marks,
        fqus,fmarks,filltype
        '''

        fdata = zip(fqus,filltype,fmarks,filltypeusermarks)
        data = zip(questions,option1,option2,option3,option4,mymcqans,rightmcqans,gained_marks,marks)


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