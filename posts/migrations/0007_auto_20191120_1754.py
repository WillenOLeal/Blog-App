# Generated by Django 2.2.5 on 2019-11-20 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20191119_1519'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='authror',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='visualization',
            old_name='authror',
            new_name='author',
        ),
    ]
