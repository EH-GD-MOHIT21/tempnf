from django.shortcuts import redirect, render
from quizform.models import QuizManager, base_submitted_form_data

# Create your views here.

def RenderSurveyForQuiz(request,quiz_id):
    if not request.user.is_authenticated:
        return redirect('/login')
    try:
        code = QuizManager.objects.get(token=quiz_id)
    except:
        return render(request,'confirm.html',{'message':'Quiz Not Exists with provided id.'})
    
    rcode = base_submitted_form_data.objects.filter(token=quiz_id)
    if not len(rcode):
        return render(request,'confirm.html',{'message':'No Response exists to be analyse'})
    # here data will be collected from db and show on web.
    return render(request,'nf_survey.html')