# Generated by Django 3.2.12 on 2022-04-22 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_user_has_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='serial_number',
            field=models.CharField(default='', max_length=128, unique=True),
        ),
    ]
