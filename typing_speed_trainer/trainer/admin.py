from django.contrib import admin

from trainer.models import Statistic


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    fields = ['user', 'attempts_amount', 'average_wpm', 'average_accuracy']
    search_fields = ['attempts_amount', 'average_wpm', 'average_accuracy']
    ordering = ['attempts_amount', 'average_accuracy']
