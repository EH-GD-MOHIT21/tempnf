# Generated by Django 3.2 on 2021-11-18 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizform', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizfilltypequestions',
            name='marks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quizmcqquestions',
            name='marks',
            field=models.IntegerField(default=0),
        ),
    ]
