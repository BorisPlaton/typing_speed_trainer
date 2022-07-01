import json

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from trainer.models import Statistic
from trainer.utils.mixins import TrainerResultCacheMixin
from trainer.utils.shortcuts import get_correct_template_path


class TypingTrainer(TemplateView):
    """Страница с тренажером скорости печати."""
    template_name = 'trainer/typing_trainer.html'


@method_decorator(login_required, name='dispatch')
class ResultsList(TrainerResultCacheMixin):
    """
    Принимает POST-запрос с результатами пользователя и кеширует их.
    Также отдает данные в виде JSON о результатах пользователя. Если есть
    параметр `templates`, который равен `true`, также отдает html-шаблоны
    списка результатов и самих результатов.
    """

    def get(self, request):
        data = self.get_result_templates() if request.GET.get('templates') == 'true' else {}
        data.update({
            'resultsData': self.get_all_results_from_cache(),
        })
        return JsonResponse(data)

    def post(self, request):
        """
        Кеширует данные из запроса и отправляет ответ в виде JSON
        с этими же данными.
        """
        data: dict = json.loads(request.body)
        self.update_user_data(data['wpm'], data['typingAccuracy'])
        self.cache_result_data(data)
        return JsonResponse({
            'result': self.get_result_from_cache(
                self.get_current_result_id()
            )
        })

    def update_user_data(self, wpm: int, typing_accuracy: float):
        """
        Обновляет поля `user.attempts_amount`, `user.attempts_amount` и
        `user.attempts_amount` модели `User`.
        """
        statistic = Statistic.objects.get(user=self.request.user)
        statistic.average_wpm = statistic.calculate_average_value_with(
            'average_wpm', wpm
        )
        statistic.average_accuracy = round(statistic.calculate_average_value_with(
            'average_accuracy', typing_accuracy
        ), 2)
        statistic.attempts_amount = F('attempts_amount') + 1
        statistic.save()

    def dispatch(self, request, *args, **kwargs):
        self.user_pk = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def get_result_templates() -> dict:
        with (
            open(get_correct_template_path(
                'trainer', 'includes', 'results_list.html'
            )) as list_template_file,
            open(get_correct_template_path(
                'trainer', 'includes', 'last_result.html'
            )) as res_template_file,
        ):
            results_list_template = list_template_file.read()
            result_template = res_template_file.read()
        return {
            'resultsListTemplate': results_list_template,
            'resultTemplate': result_template,
        }
