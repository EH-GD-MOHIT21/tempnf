# Generated by Django 3.2 on 2021-11-19 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizform', '0005_base_submitted_form_data_filltypeuserresponses_mcqtypeuserresponses'),
    ]

    operations = [
        migrations.AddField(
            model_name='filltypeuserresponses',
            name='final_marks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mcqtypeuserresponses',
            name='final_marks',
            field=models.IntegerField(default=0),
        ),
    ]
