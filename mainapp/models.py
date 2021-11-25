from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class formpublicdata(models.Model):
    token = models.CharField(max_length=100,unique=True)
    title = models.CharField(max_length=100)
    mail = models.EmailField()
    creator = models.CharField(max_length=40)
    desc = models.TextField()
    show_response = models.BooleanField(default=False)
    accept_response = models.BooleanField(default=True)


class formMCQquestions(models.Model):
    code = models.ForeignKey(formpublicdata,on_delete=models.CASCADE)
    question = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    option4 = models.TextField()
    is_multi_correct = models.BooleanField(default=False)


class formFillTypeQuestions(models.Model):
    code = models.ForeignKey(formpublicdata,on_delete=models.CASCADE)
    question = models.TextField()


class base_form_data_response(models.Model):
    token = models.CharField(max_length=100)
    name = models.CharField(max_length=40)
    email = models.EmailField()
    phone_no = models.CharField(max_length=12)
    address = models.CharField(max_length=100)

    def __str__(self):
        return "FormId: "+self.token


class formFillTypeResponse(models.Model):
    code = models.ForeignKey(base_form_data_response,on_delete=models.CASCADE)
    answer = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.code)


class formMCQTypeResponse(models.Model):
    code = models.ForeignKey(base_form_data_response,on_delete=models.CASCADE)
    answer = models.TextField(null=True,blank=True)
    def __str__(self):
        return str(self.code)

