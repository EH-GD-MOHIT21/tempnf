from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from mainapp.models import *
import ast
import pandas as pd
from django.conf import settings
import os



@csrf_exempt
def Create_Csv_Resp_forms(request):
    if not request.user.username or not request.method == "POST":
        return JsonResponse({'status':400,'message':'Invalid Request.'})
    
    body = json.loads(request.body)
    email = request.user.email
    form_id = body.get("form_id")

    try:
        code = formpublicdata.objects.get(token=form_id)
    except:
        return JsonResponse({'status':404,'message':'Required form does not exists.'})

    base_form_resp = base_form_data_response.objects.filter(token=form_id)
    if not len(base_form_resp):
        return JsonResponse({'status':406,'message':'There should be atleast 1 response to fetch csv.'})

    mcqqus = formMCQquestions.objects.filter(code=code)
    ftpqus = formFillTypeQuestions.objects.filter(code=code)
    names = []
    emails = []
    phone_no = []
    address = []
    mcq_qus = []
    ftp_qus = []
    for data in base_form_resp:
        names.append(data.name)
        emails.append(data.email)
        phone_no.append(data.phone_no)
        address.append(data.address)

    for qus in mcqqus:
        mcq_qus.append(qus.question)

    for qus in ftpqus:
        ftp_qus.append(qus.question)

    ftp_ans = []
    mcq_ans = []
    
    for resp in base_form_resp:
        ans = []
        for obj in formFillTypeResponse.objects.filter(code=resp):
            ans.append(obj.answer)
        ftp_ans.append(ans)

    for resp in base_form_resp:
        ans = []
        for obj in formMCQTypeResponse.objects.filter(code=resp):
            new_list = ast.literal_eval(obj.answer)
            new_list = list(set(new_list))
            if '' in new_list:
                new_list.remove('')
            ans.append(new_list)
        mcq_ans.append(ans)


    d = {}
    d['name'] = names
    d['email'] = emails
    d['phone_no'] = phone_no
    d['address'] = address
    for qus in ftp_qus:
        d[qus] = []
        for i in names:
            d[qus].append(None)
    for qus in mcq_qus:
        d[qus] = []
        for i in names:
            d[qus].append(None)
    for i in range(len(ftp_ans)):
        for j in range(len(ftp_qus)):
            d[ftp_qus[j]][i] = ftp_ans[i][j]
            
    for i in range(len(mcq_ans)):
        for j in range(len(mcq_qus)):
            d[mcq_qus[j]][i] = mcq_ans[i][j]

    df = pd.DataFrame(d)
    df.to_csv(os.path.join(settings.BASE_DIR,f'media/{form_id}.csv'),index=False)
    filepath =  "/media/" + form_id+".csv"
    return JsonResponse({'status':200,'message':'success','path':filepath})