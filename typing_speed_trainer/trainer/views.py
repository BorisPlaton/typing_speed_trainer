import json

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from account.models import User
from common.mixins import ResultsFormattingMixin
from trainer.models import Statistic
from trainer.utils.decorators import json_request_required
from trainer.utils.cache_results import TrainerResultCache, AllUserResultsMixin


class TypingTrainer(TemplateView, ResultsFormattingMixin, AllUserResultsMixin):
    """Страница с тренажером скорости печати."""
    template_name = 'trainer/typing_trainer.html'
    user_model = User.objects.select_related('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_users_results'] = self.get_formatted_date_end_results(
            self.get_last_cached_results(10, with_users=True)
        )[::-1]
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(json_request_required, name='post')
class ResultsList(View, AllUserResultsMixin, TrainerResultCache):
    """
    Принимает POST-запрос с результатами пользователя и кеширует их.
    Также отдает данные в виде JSON о результатах пользователя. Если есть
    параметр `templates`, который равен `true`, также отдает html-шаблоны
    списка результатов и самих результатов.
    """

    def get(self, request):
        """
        Возвращает данные пользователя из кэша, если требуется, и
        html-шаблоны результатов.
        """
        data = self.get_result_templates() if request.GET.get('templates') == 'true' else {}
        data.update({
            'resultsData': self.get_all_current_user_results()[::-1],
        })
        return JsonResponse(data, status=200)

    def post(self, request):
        """
        Кеширует данные из запроса и отправляет ответ в виде JSON
        с этими же данными, если полученные данные корректны.
        """
        data: dict = json.loads(request.body)
        if self.is_correct_user_typing_result_data(data):
            self.update_user_statists_model(data['wpm'], data['typingAccuracy'])
            self.cache_result_data(data)

            if self.request.user.profile.are_results_shown:
                self.add_to_last_cached_results(self.user_id, self.current_user_result_id)

            return JsonResponse({'result': data})
        return JsonResponse({
            'status': 'Некорректные данные',
            'data': data,
        }, status=400)

    def update_user_statists_model(self, wpm: int, typing_accuracy: float):
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
        """
        Присваивает `user_id` значение `id` пользователя для корректной
        работы миксина `TrainerResultCacheMixin`.
        """
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def get_result_templates() -> dict:
        """
        Возвращает шаблоны результата и списка результатов в виде словаря
        с ключами `resultsListTemplate` и `resultTemplate`.
        """
        return {
            'resultsListTemplate': render_to_string('trainer/includes/results_list.html'),
            'resultTemplate': render_to_string('trainer/includes/last_result.html'),
        }
