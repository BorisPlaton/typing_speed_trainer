import json

from django.core.cache import cache
from django.http import JsonResponse
from django.utils import timezone
from django.views import View


class TrainerResultMixin(View):

    def post(self, request):
        data: dict = json.loads(request.body)
        self.cache_result_data(data)
        return JsonResponse({
            'result': self.get_result_from_cache(
                self.get_current_result_id()
            )
        })

    def cache_result_data(self, data: dict):
        """Кеширует результат тренажера."""
        new_id = self.get_and_increment_new_result_id()
        data.update({
            'date': timezone.now()
        })
        cache.set(f'result:{new_id}', data)

    def get_all_results_from_cache(self) -> list[dict | None]:
        """
        Возвращает все записи результатов. Если таких ещё нет, вернет
        пустой список.
        """
        results = []
        current_id = self.get_current_result_id()

        if not current_id:
            return results

        for res_id in range(1, self.get_current_result_id() + 1):
            result = self.get_result_from_cache(res_id)
            if result:
                results.append(result)

        return results

    @staticmethod
    def get_result_from_cache(result_id: int) -> dict | bool:
        """
        Возвращает данные результата по ключу `result_id`. Если
        их нет, вернет `False`.
        """
        return cache.get(f'result:{result_id}', False)

    @staticmethod
    def get_current_result_id() -> int | None:
        """
        Возвращает текущий `id` ключа результата. Если такого
        ещё нет, возвращает `None`.
        """
        return cache.get('results_id')

    @staticmethod
    def get_and_increment_new_result_id() -> int:
        if not cache.get('results_id'):
            cache.set('results_id', 0, None)
        result_id: int = cache.incr("results_id")
        return result_id
