from django.db.models import F
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import UpdateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from account.models import User
from trainer.models import Statistic
from trainer.utils.cache_results import CacheResultSet


class ResultsList(UpdateModelMixin, ListModelMixin, CacheResultSet, GenericViewSet):
    """
    Принимает POST-запрос с результатами пользователя и кеширует их.
    Также отдает данные в виде JSON о результатах пользователя.
    """

    user_models = User.objects.select_related('profile')
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """Возвращает результаты пользователя из кэша."""
        results_data = self.get_all_current_user_results()
        data = {
            'resultsData': results_data,
        }
        return Response(data)

    def create(self, request: Request):
        """
        Кеширует данные из запроса и отправляет ответ в виде JSON
        с этими же данными, если полученные данные корректны.
        """
        data = request.data
        if not self.is_correct_user_typing_result_data(data):
            return Response({
                'details': 'Некорректные данные',
                'data': data,
            }, status=400)
        self.update_user_statists_model(data['wpm'], data['typingAccuracy'])
        self.cache_result_data(data)
        self.add_to_last_cached_results(self.user_id, self.current_user_result_id)
        return Response({'status': 'OK'})

    def add_to_last_cached_results(self, user_id, result_id):
        """
        Добавляет в список последних результатов данные
        пользователя, если он разрешил сохранить их.
        """
        if self.request.user.profile.are_results_shown:
            super().add_to_last_cached_results(self.user_id, self.current_user_result_id)

    def update_user_statists_model(self, wpm: int, typing_accuracy: float):
        """Обновляет поля модели `Statistic`."""
        statistic = Statistic.objects.get(user=self.request.user)
        statistic.wpm = statistic.calculate_average_value_with(
            'wpm', wpm
        )
        statistic.accuracy = round(statistic.calculate_average_value_with(
            'accuracy', typing_accuracy
        ), 2)
        statistic.attempts_amount = F('attempts_amount') + 1
        statistic.save()

    def dispatch(self, request, *args, **kwargs):
        """
        Присваивает `user_id` значение `id` пользователя для
        корректной работы миксина `TrainerResultCache`.
        """
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def result_template(request: Request):
    """
    Возвращает шаблон результата и дополнительный шаблон
    списка, если пользователь указал это в параметрах запроса.
    """
    data = {
        'resultTemplate': render_to_string('trainer/includes/last_result.html')
    }
    if request.query_params.get('list') == 'true':
        data.update({
            'resultsListTemplate': render_to_string('trainer/includes/results_list.html')
        })
    return Response(data=data)
