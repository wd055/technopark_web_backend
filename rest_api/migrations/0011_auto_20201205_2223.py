# Generated by Django 3.1.3 on 2020-12-05 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0010_auto_20201205_1631'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='author',
            new_name='user',
        ),
    ]
