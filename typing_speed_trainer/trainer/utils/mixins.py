from datetime import datetime

from django.core.cache import cache

from trainer.utils.datastructures import UserTypingResult, ResultFieldType


class TrainerResultCacheMixin:
    """
    Миксин для работы с кешем данных результатов тренажера определенного
    пользователя. Для того, чтоб класс корректно работал, нужно указать
    в атрибут класса `user_pk` поле модели `id` пользователя. По умолчанию
    атрибут имеет значение `None`.
    """

    user_pk: int = None

    def cache_result_data(self, data: UserTypingResult) -> None:
        """Кеширует результат определенного пользователя."""
        new_id = self.get_and_increment_new_result_id()
        cache.set(f'result:{new_id}', data, version=self.user_pk)

    def clean_user_cached_data(self) -> int:
        """
        Очищает все данные результатов пользователя из кэша
        и возвращает количество удаленных ключей.
        """
        result_keynames = self.get_all_cache_keynames()
        if result_keynames:
            cache.delete_many(result_keynames, version=self.user_pk)
        return len(result_keynames)

    def get_all_results_from_cache(self) -> list[UserTypingResult | None]:
        """
        Возвращает все записи результатов пользователя. Если таких ещё нет,
        вернет пустой список.
        """
        result_keynames = self.get_all_cache_keynames()
        results: dict = cache.get_many(result_keynames, version=self.user_pk)
        return [result for result in results.values()]

    def get_result_from_cache(self, result_id: int) -> UserTypingResult | bool:
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

    def get_all_cache_keynames(self) -> list[str | None]:
        """Возвращает все ключи данных из кэша, если таковы есть."""
        current_id = self.get_current_result_id()

        if not current_id:
            return []

        result_key_names = [f'result:{result_id}' for result_id in range(1, current_id + 1)]

        return result_key_names

    @staticmethod
    def is_correct_user_typing_result_data(outer_data: dict) -> bool:
        """Делает валидацию полученных данных."""
        result_data_fields = [
            ResultFieldType('invalidKeystrokes', int),
            ResultFieldType('correctKeystrokes', int),
            ResultFieldType('summaryKeystrokes', int),
            ResultFieldType('invalidWordsAmount', int),
            ResultFieldType('correctWordsAmount', int),
            ResultFieldType('totalWordsAmount', int),
            ResultFieldType('typingAccuracy', float | int),
            ResultFieldType('wpm', int),
            ResultFieldType('dateEnd', str),
        ]

        for result_data_field in result_data_fields:
            field = outer_data.get(result_data_field.field_name)
            if result_data_field.field_name == 'dateEnd':
                try:
                    datetime.strptime(field, '%Y-%m-%dT%H:%M:%S.%fZ')
                except ValueError:
                    return False
            elif not isinstance(field, result_data_field.field_type):
                return False

        return True
