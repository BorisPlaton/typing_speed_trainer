# Generated by Django 4.0.5 on 2022-07-01 02:30

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=16, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Имя пользователя'),
        ),
    ]
