# Generated by Django 3.2 on 2021-11-30 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20211127_0020'),
    ]

    operations = [
        migrations.AddField(
            model_name='formpublicdata',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
