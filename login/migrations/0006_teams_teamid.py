# Generated by Django 3.0.5 on 2020-04-28 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_remove_teams_teamid'),
    ]

    operations = [
        migrations.AddField(
            model_name='teams',
            name='teamid',
            field=models.IntegerField(default=0),
        ),
    ]
