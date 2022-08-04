import math

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from account.models import User


class Statistic(models.Model):
    """Модель статистики пользователя"""

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
        verbose_name = "Статистика"
        verbose_name_plural = "Статистики"

    def calculate_average_value_with(self, field_name: str, value: float) -> float:
        current_field_value = getattr(self, field_name)
        new_field_value = (current_field_value * self.attempts_amount + value) / (self.attempts_amount + 1)
        return new_field_value

    @property
    def correct_chars_amount(self) -> int:
        """
        Возвращает количество правильных символов за одну
        сессию набора текста. Значение есть производным от
        других значений.
        """
        return math.floor(self.wpm * 5 * self.accuracy / 100)

    @property
    def typo_amount(self) -> int:
        """
        Возвращает количество опечаток. Значение является
        приблизительным и высчитывается из значения скорости
        набора текста и аккуратности печати.
        """
        return math.ceil(self.wpm * 5 * (100 - self.accuracy) / 100)

    def __str__(self):
        return f"{self.attempts_amount} - {self.accuracy}"
