# Generated by Django 2.2.1 on 2020-07-04 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
        ('Match', '0001_initial'),
        ('Pick', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pick',
            unique_together={('UID', 'MID')},
        ),
    ]