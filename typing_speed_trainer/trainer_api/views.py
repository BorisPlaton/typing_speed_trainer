from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import UpdateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from trainer_api.services import get_all_user_results, update_and_cache_user_typing_result
from type_results.results_handlers import UserTypingResult


class ResultsList(UpdateModelMixin, ListModelMixin, GenericViewSet):
    """
    Принимает POST-запрос с результатами пользователя и кеширует их.
    Также отдает данные в виде JSON о результатах пользователя.
    """

    permission_classes = [IsAuthenticated]

    def list(self, request: Request, *args, **kwargs):
        """Возвращает результаты пользователя из кэша."""
        return Response({'resultsData': get_all_user_results(request.user.pk)})

    def create(self, request: Request):
        """
        Кеширует данные из запроса и отправляет ответ в виде JSON
        с этими же данными, если полученные данные корректны.
        """
        try:
            typing_statistics = UserTypingResult(**request.data)
        except Exception as e:
            return Response({'details': 'Некорректные данные', 'data': str(e)}, status=400)
        update_and_cache_user_typing_result(request.user.id, typing_statistics)
        return Response({'status': 'OK'})


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def result_template(request: Request):
    """
    Возвращает шаблон результата и дополнительный шаблон
    списка, если пользователь указал это в параметрах запроса.
    """
    data = {'resultTemplate': render_to_string('trainer/includes/last_result.html')}
    if request.query_params.get('list') == 'true':
        data.update({
            'resultsListTemplate': render_to_string('trainer/includes/results_list.html')
        })
    return Response(data=data)
