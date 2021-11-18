from django.shortcuts import redirect, render
from .app_utils.model_manager import *
from .models import *
import ast

# Create your views here.

def RenderCreateQuiz(request):
    if request.user.is_authenticated:
        return render(request,'createquiz.html')
    else:
        return redirect('/login')


def SaveQuiz(request):
    if request.method == "POST" and request.user.is_authenticated:
        token,model = QuizManagerObjectCreator(request)
        MCQTypeQuestionSaver(request,model)
        FillTypeQuestionSaver(request,model)
        # ans of quizes may be empty
        MCQTypeAnswerSaver(request,model)
        print(token)
        return redirect('/createquiz')
    else:
        return redirect('/login')


def FillQuiz(request,quiz_id):
    if not request.user.is_authenticated:
        return redirect('/login')

    try:
        base_submitted_form_data.objects.get(token=quiz_id,email=request.user.email)
        return redirect('/')
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
        return redirect('/')
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

    return redirect('/fillquiz/UzKcvzr4h7aeZh2M1xEp4KEDYjmcgAwQDV4F0c7jTchqH1NLLssW96R1h2021_11_18_16_44_02_961052')



def ManageQuizes(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    quizzes_codes = []
    all_quizes = base_submitted_form_data.objects.filter(email=request.user.email)
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
        for obj in filltypesubmitted:
            filltype.append(obj.answer)

        mcqtypesubmitted = MCQTypeUserResponses.objects.filter(code=responses_obj)
        real_ans = QuizMCQAnswers.objects.filter(code=quiz)

        gained_marks = []

        mymcqans = []
        rightmcqans = []
        
        for index,obj in enumerate(mcqtypesubmitted):
            mark = 0
            userfilled = ast.literal_eval(obj.answer)
            right_ans = ast.literal_eval(real_ans[index].answers)
            print(userfilled,right_ans)
            mymcqans.append(userfilled)
            rightmcqans.append(right_ans)

            for value in userfilled:
                if value in right_ans and value != '':
                    mark += (marks[index]/len(right_ans))
            gained_marks.append(mark)
        
        # permission <<<->>>

        '''
        questions,option1-4
        mymcqans,rightmcqans,gained_marks,marks,
        fqus,fmarks,filltype
        '''

        fdata = zip(fqus,filltype,fmarks)
        data = zip(questions,option1,option2,option3,option4,mymcqans,rightmcqans,gained_marks,marks)


        if (email == request.user.username) or (quiz.mail==request.user.username) or (request.user.is_superuser):
            return render(request,'quizresponse.html',{'title':title,'desc':desc,'author':author,'contact':contact,'data':data,'username':username,'mail':mail,'phone':phone,'address':address,'date':date,'fdata':fdata})
        
        return render(request,'confirm.html',{'message':'You Cannot see someone others responses.'})

    except Exception as e:
        print(e)
        return redirect('/')