# Generated by Django 2.2.5 on 2019-11-05 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='thumbnail',
        ),
    ]