# Generated by Django 3.1.3 on 2020-12-28 00:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0027_auto_20201228_0408'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-date'], 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
    ]
