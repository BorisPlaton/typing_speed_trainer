import json

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from trainer.models import Statistic
from trainer.utils.decorators import json_request_required
from trainer.utils.mixins import TrainerResultCacheMixin, AllUserResultsMixin
from trainer.utils.shortcuts import get_correct_template_path


class TypingTrainer(TemplateView, AllUserResultsMixin):
    """Страница с тренажером скорости печати."""
    template_name = 'trainer/typing_trainer.html'
    join_to_user_cache_model = ['profile']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_users_results'] = self.get_last_cached_results(10, with_users=True)

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(json_request_required, name='post')
class ResultsList(View, AllUserResultsMixin, TrainerResultCacheMixin):
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
            'resultsData': self.get_all_current_user_results_from_cache(),
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
                self.add_to_last_cached_results(self.user_pk, self.get_current_result_id())

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
        Присваивает значение `self.user_pk` `id` пользователя, для
        корректной работы `TrainerResultCacheMixin`.
        """
        self.user_pk = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def get_result_templates() -> dict:
        """
        Возвращает шаблоны результата и списка результатов в виде словаря
        с ключами `resultsListTemplate` и `resultTemplate`.
        """
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
