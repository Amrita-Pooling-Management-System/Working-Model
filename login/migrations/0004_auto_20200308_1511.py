# Generated by Django 3.0.4 on 2020-03-08 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_journey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journey',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Profile'),
        ),
    ]
