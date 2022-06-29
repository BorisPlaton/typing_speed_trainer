# Generated by Django 4.0.5 on 2022-06-28 23:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempts_amount', models.PositiveIntegerField(verbose_name='Количество попыток')),
                ('average_wpm', models.PositiveIntegerField(verbose_name='Среднее количество слов в минуту')),
                ('average_typo_amount', models.PositiveIntegerField(verbose_name='Среднее количество ошибок')),
                ('average_accuracy', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='Средняя точность набора текста')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='static', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Статистика',
                'verbose_name_plural': 'Статистики',
            },
        ),
    ]
