# Generated by Django 2.2.6 on 2020-06-16 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GID', models.CharField(max_length=256, unique=True)),
            ],
        ),
    ]
