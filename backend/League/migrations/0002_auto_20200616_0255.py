# Generated by Django 2.2.6 on 2020-06-16 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('League', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='sportName',
            field=models.TextField(choices=[('SOCCER', 'SOCCER'), ('MMA', 'MMA'), ('FOOTBALL', 'FOOTBALL'), ('BASEBALL', 'BASEBASS')]),
        ),
    ]