# Generated by Django 2.2.6 on 2020-06-16 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sportName', models.CharField(max_length=128)),
                ('leagueName', models.CharField(max_length=256)),
            ],
        ),
    ]
