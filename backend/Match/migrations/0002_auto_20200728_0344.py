# Generated by Django 2.2.1 on 2020-07-28 03:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Participant', '0003_auto_20200618_0431'),
        ('Match', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='match',
            unique_together={('team1', 'team2', 'date')},
        ),
    ]
