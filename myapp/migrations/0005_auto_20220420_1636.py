# Generated by Django 3.2.12 on 2022-04-20 16:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_user_has_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_confirmed',
            field=models.CharField(default='N', max_length=1),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='', max_length=16, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')]),
        ),
    ]
