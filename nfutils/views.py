from django.http import JsonResponse
from django.shortcuts import render
from quizform.models import QuizManager, base_submitted_form_data
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from mainapp.models import base_form_data_response, formFillTypeResponse, formMCQTypeResponse, formpublicdata,formMCQquestions,formFillTypeQuestions

# Create your views here.

# release quiz score api here

@csrf_exempt
def ReleaseQuizScoreApi(request):
    # if not request.user.is_authenticated or not request.method == "POST":
    #     return JsonResponse({'status':400,'message':'Invalid Request.'})
    try:
        body = json.loads(request.body)
        quiz_id = body.get("quiz_id")
    except:
        return JsonResponse({'status':400,'message':'Invalid Request.'})
    try:
        quiz = QuizManager.objects.get(token=quiz_id)
    except:
        return JsonResponse({'status':404,'message':'Quiz Not Exists.'})
    # if quiz.mail != request.user.email:
    #     return JsonResponse({'status':406,'message':'You donot have sufficient permission to release marks.'})
    responses = base_submitted_form_data.objects.filter(token=quiz_id)
    emailbodies = []
    for res in responses:
        message = []
        message.append(f"Hello {res.name}, Score Released For Quiz @ NestedForms.com")
        message.append(f"To see Your Responses and marks Please Click on the provided link\n\n {settings.SITE_URL}showquizresponses/{quiz_id}/filter?email={res.email}\n\n\n\nThanks & Regards\nNestedForms.com")
        message.append(settings.EMAIL_SENDER)
        message.append([res.email])
        emailbodies.append(message)
    # better way -> save these info in a new model
    # schedule task and send mails also delete its objects.
    send_mass_mail(emailbodies, fail_silently=False,auth_user=settings.EMAIL_SENDER,auth_password=settings.PASS_SENDER)
    return JsonResponse({'status':200,'message':'success'})



def UpdateForm(request,form_id):
    if not request.method == "POST" or not request.user.is_authenticated:
        return render(request,'confirm.html',{'message':'User Not Authorised'})
    try:
        form = formpublicdata.objects.get(token=form_id)
    except:
        return render(request,'confirm.html',{'message':'Form Not Exists.'})
    if form.mail != request.user.email:
        return render(request,'confirm.html',{'message':'You need suffiecient permissions to update this form.'})
    form.title = request.POST["formtitle"]
    form.creator = request.POST["creatorname"]
    form.desc = request.POST["formdesc"]
    form.save()
    questionmcqs = request.POST.getlist("questionmcq")
    option1 = request.POST.getlist("option1")
    option2 = request.POST.getlist("option2")
    option3 = request.POST.getlist("option3")
    option4 = request.POST.getlist("option4")
    multi = request.POST.getlist("multicorrect")

    for index,qus in enumerate(questionmcqs):
        model = formMCQquestions()
        model.code = form
        model.question = qus
        model.option1 = option1[index]
        model.option2 = option2[index]
        model.option3 = option3[index]
        model.option4 = option4[index]
        if multi[index].strip() == "1":
            model.is_multi_correct = True
        else:
            model.is_multi_correct = False
        model.save()

    ftpqus = request.POST.getlist("questionftp")
    for qus in ftpqus:
        model = formFillTypeQuestions()
        model.question = qus
        model.code = form
        model.save()


    return render(request,'confirm.html',{'message':'Your form has been successfully updated.'})


def RenderUpdateForm(request,form_id):
    try:
        form = formpublicdata.objects.get(token=form_id)
    except:
        return render(request,'confirm.html',{'message':'form does not exists.'})
    if not request.user.is_authenticated or form.mail != request.user.email:
        return render(request,'confirm.html',{'message':'You are not authorised to update form.'})
    mcq_qus = formMCQquestions.objects.filter(code=form)
    ftpqus = formFillTypeQuestions.objects.filter(code=form)
    print(mcq_qus,ftpqus)
    data = {
        "title":form.title,
        "email":form.mail,
        "creator":form.creator,
        "desc":form.desc,
        "mcqqus":mcq_qus,
        "ftpqus":ftpqus,
        "id":form_id
    }
    return render(request,'update_form.html',data)
    
@csrf_exempt
def delmcqform(request):
    if not request.user.is_authenticated or request.method != "POST":
        return JsonResponse({'status':403,"message":"Invalid Request."})
    body = json.loads(request.body)
    form_id = body.get("form_id")
    try:
        qus_id = int(body.get("qus_id"))
    except:
        return JsonResponse({'status':400,'message':'Invalid question id.'})
    try:
        form = formpublicdata.objects.get(token=form_id)
    except:
        return JsonResponse({'status':400,'message':'form not found.'})
    if request.user.email != form.mail:
        return JsonResponse({'status':403,'message':"You need permissions."})
    # delete form question and responses
    fmcqs = formMCQquestions.objects.filter(code=form)
    fmcqs[qus_id].delete()
    base_form_res = base_form_data_response.objects.filter(token=form_id)
    for res in base_form_res:
        mcqres = formMCQTypeResponse.objects.filter(code=res)
        mcqres[qus_id].delete()

    return JsonResponse({'status':200,'message':'success'})


@csrf_exempt
def delformftp(request):
    if not request.user.is_authenticated or request.method != "POST":
        return JsonResponse({'status':403,"message":"Invalid Request."})
    body = json.loads(request.body)
    form_id = body.get("form_id")
    try:
        qus_id = int(body.get("qus_id"))
    except:
        return JsonResponse({'status':400,'message':'Invalid question id.'})
    
    try:
        form = formpublicdata.objects.get(token=form_id)
    except:
        return JsonResponse({'status':400,'message':'form not found.'})
    if request.user.email != form.mail:
        return JsonResponse({'status':403,'message':"You need permissions."})
    
    fmcqs = formFillTypeQuestions.objects.filter(code=form)
    fmcqs[qus_id].delete()
    base_form_res = base_form_data_response.objects.filter(token=form_id)
    for res in base_form_res:
        mcqres = formFillTypeResponse.objects.filter(code=res)
        mcqres[qus_id].delete()

    return JsonResponse({'status':200,'message':'success'})