# Generated by Django 3.2 on 2021-12-09 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizform', '0012_auto_20211128_2346'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizmanager',
            name='negative_marking_scheme',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
