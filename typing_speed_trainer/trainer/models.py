from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from account.models import User


class Statistic(models.Model):
    """Модель статистики пользователя"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='static',
        verbose_name="Пользователь"
    )
    attempts_amount = models.PositiveIntegerField("Количество попыток")
    average_wpm = models.PositiveIntegerField("Среднее количество слов в минуту")
    average_typo_amount = models.PositiveIntegerField("Среднее количество ошибок")
    average_accuracy = models.FloatField(
        "Средняя точность набора текста",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1),
        ]
    )

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистики"

    def __str__(self):
        return f"{self.attempts_amount} - {self.average_accuracy}"
