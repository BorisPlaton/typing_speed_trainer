from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import UpdateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from trainer_api.services import update_and_cache_user_typing_result
from type_results.services import get_all_user_results
from type_results.structs import UserTypingResult


class ResultsList(UpdateModelMixin, ListModelMixin, GenericViewSet):
    """
    Receives a POST-request with user's results and caches them.
    Also, it can send user's statistics in the JSON format.
    """

    permission_classes = [IsAuthenticated]

    def list(self, request: Request, *args, **kwargs):
        """Returns users statistics from the cache."""
        return Response(
            {'resultsData': [vars(result) for result in get_all_user_results(request.user.pk)]}
        )

    def create(self, request: Request):
        """
        Caches received user's statistics if it is in the correct
        form.
        """
        try:
            typing_statistics = UserTypingResult(**request.data)
        except Exception as e:
            return Response({'details': 'Invalid data', 'data': str(e)}, status=400)
        update_and_cache_user_typing_result(request.user.id, typing_statistics)
        return Response({'status': 'OK'})


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def result_template(request: Request):
    """
    Returns the template of result and an additional template
    with results list if it is specified it the query parameters.
    """
    data = {'resultTemplate': render_to_string('trainer/includes/last_result.html')}
    if request.query_params.get('list') == 'true':
        data.update({
            'resultsListTemplate': render_to_string('trainer/includes/results_list.html')
        })
    return Response(data=data)
