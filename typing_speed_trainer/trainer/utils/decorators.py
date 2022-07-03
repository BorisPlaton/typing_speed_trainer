from functools import wraps

from django.http import JsonResponse


def json_request_required(func):
    """
    Проверяет, что запрос имеет заголовок 'Content type', который
    равен 'application/json'.
    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.content_type == 'application/json':
            return func(request, *args, **kwargs)
        return JsonResponse({'status': "Заголовок запроса 'Content type' не равен 'application/json'"}, status=412)

    return wrapper
