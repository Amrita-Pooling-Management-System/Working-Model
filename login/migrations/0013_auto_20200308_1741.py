# Generated by Django 3.0.4 on 2020-03-08 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0012_journey'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(default=987654321, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='journey',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]