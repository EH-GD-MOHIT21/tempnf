# Generated by Django 3.2 on 2021-11-22 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizform', '0009_auto_20211122_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizmanager',
            name='show_response',
            field=models.BooleanField(default=False),
        ),
    ]
