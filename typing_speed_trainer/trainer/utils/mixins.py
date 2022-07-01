import json

from django.core.cache import cache
from django.http import JsonResponse
from django.views import View


class TrainerResultMixin(View):
    """
    Миксин для работы с кешем данных результатов тренажера определенного
    пользователя. Для того, чтоб класс корректно работал, нужно указать
    в атрибут класса `user_pk` поле модели `id` пользователя. По умолчанию
    атрибут имеет значение `None`.
    """

    user_pk: int = None

    def post(self, request):
        data: dict = json.loads(request.body)
        self.cache_result_data(data)
        return JsonResponse({
            'result': self.get_result_from_cache(
                self.get_current_result_id()
            )
        })

    def cache_result_data(self, data: dict):
        """Кеширует результат определенного пользователя."""
        new_id = self.get_and_increment_new_result_id()
        cache.set(f'result:{new_id}', data, version=self.user_pk)

    def get_all_results_from_cache(self) -> list[dict | None]:
        """
        Возвращает все записи результатов пользователя. Если таких ещё нет,
        вернет пустой список.
        """
        current_id = self.get_current_result_id()

        if not current_id:
            return []

        result_key_names = [f'result:{result_id}' for result_id in range(1, current_id + 1)]
        results: dict = cache.get_many(result_key_names, version=self.user_pk)

        return [result for result in results.values()]

    def get_result_from_cache(self, result_id: int) -> dict | bool:
        """
        Возвращает данные результата по ключу `result_id`. Если
        их нет, вернет `None`.
        """
        return cache.get(f'result:{result_id}', version=self.user_pk)

    def get_current_result_id(self) -> int | None:
        """
        Возвращает текущий `id` ключа результата. Если такого
        ещё нет, возвращает `None`.
        """
        return cache.get('results_id', version=self.user_pk)

    def get_and_increment_new_result_id(self) -> int:
        """
        Увеличивает значение текущего `id` результата и возвращает
        его значение. Если `id` ещё нет, то создаёт его.
        """
        if not self.get_current_result_id():
            cache.set('results_id', 0, version=self.user_pk)
        result_id: int = cache.incr("results_id", version=self.user_pk)
        return result_id
