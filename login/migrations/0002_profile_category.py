# Generated by Django 3.0.4 on 2020-03-08 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='category',
            field=models.CharField(choices=[('STUD', 'Student'), ('DRIV', 'Driver')], default='STUD', max_length=4),
        ),
    ]