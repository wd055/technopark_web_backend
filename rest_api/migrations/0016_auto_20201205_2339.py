# Generated by Django 3.1.3 on 2020-12-05 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0015_delete_pictures'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default=None, upload_to='photo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publication',
            name='photo',
            field=models.ImageField(default=None, upload_to='photo'),
            preserve_default=False,
        ),
    ]
