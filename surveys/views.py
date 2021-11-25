from django.shortcuts import redirect, render
from quizform.models import MCQTypeUserResponses, QuizMCQAnswers, QuizMCQquestions, QuizManager, base_submitted_form_data
import ast

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
    real_ans_objs = QuizMCQAnswers.objects.filter(code=code)
    final_data_Set = [[0,0,0,0] for i in range(len(real_ans_objs))]
    responses = []
    for codes in rcode:
        quizmodel = MCQTypeUserResponses.objects.filter(code=codes)
        cntr = 0
        res = 0
        for model,rmodel in zip(quizmodel,real_ans_objs):
            l1 = ast.literal_eval(model.answer)
            l2 = ast.literal_eval(rmodel.answers)
            if len(set(l1)) == 1 and l1[0] == '':
                pass
            else:
                res += 1
            for index,i in enumerate(l1):
                if i != '':
                    final_data_Set[cntr][index] += 1
            cntr += 1
        responses.append(res)

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


    return render(request,'nf_survey.html',{'data':zip(render_this,questions,normal_list,responses)})