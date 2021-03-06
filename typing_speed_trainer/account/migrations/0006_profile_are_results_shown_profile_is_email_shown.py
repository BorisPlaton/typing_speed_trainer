# Generated by Django 4.0.5 on 2022-07-04 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='are_results_shown',
            field=models.BooleanField(default=True, verbose_name='Показывать последние результаты'),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_email_shown',
            field=models.BooleanField(default=False, verbose_name='Показывать почту'),
        ),
    ]
