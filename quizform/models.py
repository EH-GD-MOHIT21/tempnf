from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class QuizManager(models.Model):
    token = models.CharField(max_length=100,unique=True)
    title = models.CharField(max_length=100,null=True,blank=True)
    mail = models.EmailField()
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    desc = models.TextField()
    date = models.DateTimeField(null=True,blank=True)
    show_response = models.BooleanField(default=False)
    accept_response = models.BooleanField(default=True)

    def __str__(self):
        return "QuizId: "+self.token

    @property
    def set_time(self):
        self.date = timezone.now()


class QuizMCQquestions(models.Model):
    code = models.ForeignKey(QuizManager,on_delete=models.CASCADE)
    marks = models.FloatField(default=0)
    question = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    option4 = models.TextField()

    def __str__(self):
        return str(self.code)


class QuizMCQAnswers(models.Model):
    code = models.ForeignKey(QuizManager,on_delete=models.CASCADE)
    option1 = models.BooleanField(default=False)
    option2 = models.BooleanField(default=False)
    option3 = models.BooleanField(default=False)
    option4 = models.BooleanField(default=False)
    answers = models.TextField(null=True,blank=True)
    def __str__(self):
        return str(self.code)

class QuizFillTypeQuestions(models.Model):
    code = models.ForeignKey(QuizManager,on_delete=models.CASCADE)
    marks = models.FloatField(default=0)
    question = models.TextField()
    def __str__(self):
        return str(self.code)



# models for save responses

class base_submitted_form_data(models.Model):
    token = models.CharField(max_length=100)
    name = models.CharField(max_length=40)
    email = models.EmailField()
    phone_no = models.CharField(max_length=12)
    address = models.CharField(max_length=100)

    def __str__(self):
        return "QuizId: "+self.token



class FillTypeUserResponses(models.Model):
    code = models.ForeignKey(base_submitted_form_data,on_delete=models.CASCADE)
    answer = models.TextField()
    final_marks = models.FloatField(default=0)

    def __str__(self):
        return str(self.code)


class MCQTypeUserResponses(models.Model):
    code = models.ForeignKey(base_submitted_form_data,on_delete=models.CASCADE)
    answer = models.TextField()
    final_marks = models.FloatField(default=0)

    def __str__(self):
        return str(self.code)


class option_survey_mcq_response(models.Model):
    code = models.ForeignKey(MCQTypeUserResponses,on_delete=models.CASCADE)
    option1 = models.FloatField(default=0)
    option2 = models.FloatField(default=0)
    option3 = models.FloatField(default=0)
    option4 = models.FloatField(default=0)
    
    def __str__(self):
        return str(self.code)