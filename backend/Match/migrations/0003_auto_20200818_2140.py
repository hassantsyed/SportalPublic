# Generated by Django 2.2.1 on 2020-08-18 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Match', '0002_auto_20200728_0344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='status',
            field=models.TextField(choices=[('UPCOMING', 'UPCOMING'), ('CANCELLED', 'CANCELLED'), ('TEAM1', 'TEAM1'), ('TEAM2', 'TEAM2'), ('TIE', 'TIE'), ('ONGOING', 'ONGOING')]),
        ),
    ]
