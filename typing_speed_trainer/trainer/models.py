import math

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from account.models import User


class Statistic(models.Model):
    """The model of user's statistics."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='statistics',
        verbose_name="Пользователь"
    )
    attempts_amount = models.PositiveIntegerField("Количество попыток", default=0)
    wpm = models.PositiveIntegerField("Среднее количество слов в минуту", default=0)
    accuracy = models.FloatField(
        "Средняя точность набора текста",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        default=0
    )

    class Meta:
        verbose_name = "Statistics"
        verbose_name_plural = "Statistics"

    @property
    def correct_chars_amount(self) -> int:
        """
        Returns the average amount of correct chars per one trainer
        attempt.
        """
        return math.floor(self.wpm * 5 * self.accuracy / 100)

    @property
    def typo_amount(self) -> int:
        """
        Returns the average amount of invalid chars per one trainer
        attempt.
        """
        return math.ceil(self.wpm * 5 * (100 - self.accuracy) / 100)

    def __str__(self):
        return f"{self.attempts_amount} - {self.accuracy}"
