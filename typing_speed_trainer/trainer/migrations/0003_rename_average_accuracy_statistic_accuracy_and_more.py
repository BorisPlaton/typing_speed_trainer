# Generated by Django 4.0.5 on 2022-08-04 07:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trainer', '0002_remove_statistic_average_typo_amount_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statistic',
            old_name='average_accuracy',
            new_name='accuracy',
        ),
        migrations.RenameField(
            model_name='statistic',
            old_name='average_wpm',
            new_name='wpm',
        ),
        migrations.AlterField(
            model_name='statistic',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
