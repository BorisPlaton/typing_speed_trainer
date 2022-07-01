import math

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from account.models import User


class Statistic(models.Model):
    """Модель статистики пользователя"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='statistic',
        verbose_name="Пользователь"
    )
    attempts_amount = models.PositiveIntegerField("Количество попыток", default=0)
    average_wpm = models.PositiveIntegerField("Среднее количество слов в минуту", default=0)
    average_accuracy = models.FloatField(
        "Средняя точность набора текста",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        default=0
    )

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистики"

    def calculate_average_value_with(self, field_name: str, value: float) -> float:
        current_field_value = getattr(self, field_name)
        new_field_value = (current_field_value * self.attempts_amount + value) / (self.attempts_amount + 1)
        return new_field_value

    @property
    def average_correct_chars_amount(self):
        return math.floor(self.average_wpm * 5 * self.average_accuracy / 100)

    @property
    def average_typo_amount(self):
        return math.ceil(self.average_wpm * 5 * (100 - self.average_accuracy) / 100)

    def __str__(self):
        return f"{self.attempts_amount} - {self.average_accuracy}"
