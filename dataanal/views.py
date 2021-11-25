from django.shortcuts import render
from .app_utils.make_csv import create_csv_base_data
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from quizform.models import FillTypeUserResponses, MCQTypeUserResponses, QuizFillTypeQuestions, QuizMCQquestions, QuizManager, base_submitted_form_data
from django.conf import settings
from .dataanal_forms import Create_Csv_Resp_forms
# Create your views here.

@csrf_exempt
def Create_Csv_User_Marks_Api(request):
    '''
    Api creates csv file at server
    with username mail and marks
    '''
    if not request.user.username or not request.method == "POST":
        return JsonResponse({'status':400,'message':'Invalid Request.'})

    body = json.loads(request.body)
    email = body.get("email")
    quiz_id = body.get("quiz_id")

    if email != request.user.email:
        return JsonResponse({'status':406,'message':'something went wrong.'})

    try:
        code = QuizManager.objects.get(token=quiz_id)
    except:
        return JsonResponse({'status':404,'message':'Quiz Not Found.'})

    code1 = base_submitted_form_data.objects.filter(token=quiz_id)
    if not len(code1):
        return JsonResponse({'status':406,'message':'There should be atleast 1 response to fetch csv.'})
    
    mcqqus = QuizMCQquestions.objects.filter(code=code)
    ftpqus = QuizFillTypeQuestions.objects.filter(code=code)
    total_marks = 0
    for qus in mcqqus:
        total_marks += qus.marks
    for qus in ftpqus:
        total_marks += qus.marks
    users = []
    final_marks_set = []
    emails = []
    for codes in code1:
        outcome = 0
        ftps = FillTypeUserResponses.objects.filter(code=codes)
        for qus in ftps:
            outcome += qus.final_marks
        mcqs = MCQTypeUserResponses.objects.filter(code=codes)
        for qus in mcqs:
            outcome += qus.final_marks
        final_marks_set.append(outcome)
        users.append(codes.name)
        emails.append(codes.email)
    create_csv_base_data(users,final_marks_set,emails,quiz_id)
    filepath =  "/media/" + quiz_id+".xlsx"
    return JsonResponse({'status':200,'message':'success','path':filepath})
