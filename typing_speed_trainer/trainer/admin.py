from django.contrib import admin

from trainer.models import Statistic


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    fields = ['user', 'attempts_amount', 'wpm', 'accuracy']
    search_fields = ['attempts_amount', 'wpm', 'accuracy']
    ordering = ['attempts_amount', 'accuracy']
