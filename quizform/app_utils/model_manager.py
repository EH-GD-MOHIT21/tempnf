from quizform.models import *
from django.conf import settings
from random import choice,randint
from datetime import datetime

def token_generator():
    chars = settings.VALID_CHARS
    length = randint(40,70)
    time_now = str(datetime.now())
    time_now = time_now.replace(':','_')
    time_now = time_now.replace('-','_')
    time_now = time_now.replace(' ','_')
    time_now = time_now.replace('.','_')

    string = ''
    for i in range(length):
        string += choice(chars)
    string += time_now

    return string


def QuizManagerObjectCreator(request):
    user = request.user
    model = QuizManager()
    model.title = request.POST["formtitle"]
    model.mail = user.email
    model.creator = user
    model.desc = request.POST["formdesc"]
    model.token = token_generator()
    model.set_time
    model.save()
    return (model.token,model)


def MCQTypeQuestionSaver(request,model_quiz):
    # for mcq based question
    marks = request.POST.getlist("markmcq")
    question = request.POST.getlist("questionmcq")
    option1 = request.POST.getlist("option1")
    option2 = request.POST.getlist("option2")
    option3 = request.POST.getlist("option3")
    option4 = request.POST.getlist("option4")

    for i in range(0,len(question)):
        model = QuizMCQquestions()
        model.code = model_quiz
        model.question = question[i]
        model.option1 = option1[i]
        model.option2 = option2[i]
        model.option3 = option3[i]
        model.option4 = option4[i]
        model.marks = marks[i]
        model.save()


def FillTypeQuestionSaver(request,model_fill):
    # for fill type questions
    marks = request.POST.getlist("markfilltype")
    fill_type_questions = request.POST.getlist("ftp") # all fill type questions at same
    for i,question in enumerate(fill_type_questions):
        model = QuizFillTypeQuestions()
        model.code = model_fill
        model.question = question
        model.marks = marks[i]
        model.save()


def MCQTypeAnswerSaver(request,model_base):
    radio1 = request.POST.getlist("radio1")
    radio2 = request.POST.getlist("radio2")
    radio3 = request.POST.getlist("radio3")
    radio4 = request.POST.getlist("radio4")

    option1 = request.POST.getlist("option1")
    option2 = request.POST.getlist("option2")
    option3 = request.POST.getlist("option3")
    option4 = request.POST.getlist("option4")

    print(radio1,radio2,radio3,radio4)

    for i in range(len(radio1)):
        model = QuizMCQAnswers()
        model.code = model_base
        answer = []
        if int(radio1[i]):
            model.option1 = True
            answer.append(option1[i])
        if int(radio2[i]):
            model.option2 = True
            answer.append(option2[i])
        if int(radio3[i]):
            model.option3 = True
            answer.append(option3[i])
        if int(radio4[i]):
            model.option4 = True
            answer.append(option4[i])
        model.answers = answer
        model.save()