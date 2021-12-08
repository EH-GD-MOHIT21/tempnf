from django.http import JsonResponse
from django.shortcuts import render
from quizform.models import QuizManager, base_submitted_form_data
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings

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