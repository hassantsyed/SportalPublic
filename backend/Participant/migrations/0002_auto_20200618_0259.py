# Generated by Django 2.2.6 on 2020-06-18 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Participant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='losses',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='participant',
            name='wins',
            field=models.IntegerField(default=0),
        ),
    ]
