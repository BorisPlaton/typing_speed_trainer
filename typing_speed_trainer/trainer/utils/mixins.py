from collections import deque
from datetime import datetime

from django.core.cache import cache

from account.models import User
from config import settings
from trainer.utils.datastructures import (
    UserTypingResult,
    ResultFieldType,
    LastUserCachedResults,
    UserTypingResultWithUser
)


class AbstractResultCache:

    @staticmethod
    def get_user_result(result_id: int, user_id: int):
        return cache.get(f'result:{result_id}', version=user_id)

    @staticmethod
    def set_user_result(result_id: int, data, user_id: int):
        cache.set(f'result:{result_id}', data, version=user_id)

    @staticmethod
    def delete_user_result(result_id: int, user_id: int):
        cache.delete(f'result:{result_id}', version=user_id)

    @staticmethod
    def get_user_current_result_id(user_id: int):
        return cache.get('results_id', version=user_id)

    @staticmethod
    def set_user_current_result_id(new_result_id, user_id: int):
        if new_result_id < 0:
            raise ValueError("`new_result_id` не может быть меньше нуля.")
        cache.set('results_id', new_result_id, version=user_id)

    def increment_current_result_id(self, user_id: int) -> int:
        if not self.get_user_current_result_id(user_id):
            self.set_user_current_result_id(0, user_id)
        return cache.incr('results_id', version=user_id)

    def get_results_keynames(self, user_id: int) -> list[str | None]:
        """Возвращает все ключи данных из кэша, если таковы есть."""
        current_id = self.get_user_current_result_id(user_id)

        if not current_id:
            return []

        result_key_names = []
        for result_id in range(current_id, 0, -1):
            if not self.get_user_result(result_id, user_id):
                break
            result_key_names.append(f'result:{result_id}')

        return result_key_names


class CurrentUserCacheMixin(AbstractResultCache):
    user_id: int = None

    @property
    def current_user_result_id(self) -> int | None:
        """
        Возвращает текущий `id` ключа результата. Если такого
        ещё нет, возвращает `None`.
        """
        return super().get_user_current_result_id(self.user_id)

    def increment_current_user_result_id(self) -> int:
        """Увеличивает текущее значение `current_user_result_id` на один."""
        return super().increment_current_result_id(self.user_id)

    def get_current_user_results_keynames(self) -> list[str | None]:
        """Возвращает все существующую ключи данных из кеша."""
        return super().get_results_keynames(self.user_id)

    def get_current_user_result(self, result_id: int):
        """
        Возвращает данные результата по ключу `result_id`. Если
        их нет, вернет `None`.
        """
        return super().get_user_result(result_id, self.user_id)

    def set_current_user_result(self, result_id: int, data):
        """Добавляет в кеш данные результата пользователя."""
        return super().set_user_result(result_id, data, self.user_id)

    def get_all_current_user_results(self):
        """
        Возвращает все записи результатов пользователя. Если таких ещё нет,
        вернет пустой список.
        """
        result_keynames = self.get_current_user_results_keynames()
        results: dict = cache.get_many(
            result_keynames, version=self.user_id
        )
        return [result for result in results.values()]

    def clean_user_results(self) -> int:
        """
        Очищает все данные результатов пользователя из кэша
        и возвращает количество удаленных ключей.
        """
        result_keynames = self.get_current_user_results_keynames()
        if result_keynames:
            cache.delete_many(result_keynames, version=self.user_id)
        return len(result_keynames)


class TrainerResultCacheMixin(CurrentUserCacheMixin):
    """
    Миксин для работы с кешем данных результатов тренажера определенного
    пользователя. Для того, чтоб класс корректно работал, нужно указать
    в атрибут класса `user_pk` поле модели `id` пользователя. По умолчанию
    атрибут имеет значение `None`.
    """

    def cache_result_data(self, data: UserTypingResult) -> None:
        """Кеширует результат определенного пользователя."""
        self.set_current_user_result(
            self.increment_current_user_result_id(),
            data,
        )

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


class AllUserResultsMixin(AbstractResultCache):
    """
    Миксин для хранения и получения последних данных результатов из кеша.
    Максимальное количество сохраненных объектов в очереди определяется
    константой `MAX_LENGTH_LAST_CACHED_DEQUE`, что задаётся в файле конфигурации.
    """

    join_to_user_cache_model: list[str] = []

    def add_to_last_cached_results(self, user_id, result_id):
        """
        Сохраняет данные о результате с полями `user_id` и `result_id`.
        """
        self._add_to_last_cached_deque(user_id=user_id, result_id=result_id)

    def get_last_cached_results(self, amount, with_users=True) -> list[UserTypingResult | UserTypingResultWithUser]:
        """
        Возвращает все последние записи результатов из кеша. В зависимости
        от аргумента `with_users` возвращает список с `UserTypingResult`
        или `UserTypingResultWithUser`.
        """
        if with_users:
            return self.get_last_cached_results_with_users(amount)
        else:
            return self.get_raw_last_cached_results(amount)

    def get_last_cached_results_with_users(self, amount: int) -> list[UserTypingResultWithUser]:
        last_results_data: list[tuple] = []
        users_pk_list: list[int] = []

        for result, _ in zip(self._get_last_cached_results(), range(amount)):
            result_from_cache: UserTypingResult = self.get_user_result(result.result_id, result.user_id)
            if result_from_cache:
                last_results_data.append(
                    (result_from_cache, result.user_id)
                )
                users_pk_list.append(result.user_id)

        if not users_pk_list:
            return []

        user_model = self._get_user_model()
        users_instance = user_model.filter(pk__in=users_pk_list)
        results_list_with_users = []

        for result_tuple in last_results_data:
            user = users_instance.filter(pk=result_tuple[1])

            if not user.exists():
                continue

            results_list_with_users.append(
                UserTypingResultWithUser(
                    user=user.first(),
                    **result_tuple[0],
                )
            )

        return results_list_with_users

    def _get_user_model(self) -> User.objects:
        user_model = User.objects

        if not self.join_to_user_cache_model:
            return user_model

        for join_model in self.join_to_user_cache_model:
            user_model = user_model.select_related(join_model)

        return user_model

    def get_raw_last_cached_results(self, amount: int) -> list[UserTypingResult]:
        """
        Возвращает список, длиной `amount` или меньше, последних данных
        результатов из кеша.

        Длина может быть меньше, так как данные результатов могли исчезнуть
        из кеша.
        """
        last_results_data: list[UserTypingResult] = []

        for result, _ in zip(self._get_last_cached_results(), range(amount)):
            result_from_cache: UserTypingResult = self.get_user_result(result.result_id, result.user_id)
            if result_from_cache:
                last_results_data.append(result_from_cache)

        return last_results_data

    def _get_last_cached_results(self) -> list[LastUserCachedResults | None]:
        last_cached_deque: deque[LastUserCachedResults] = cache.get(
            'last_cached_results',
            deque(maxlen=settings.MAX_LENGTH_LAST_CACHED_DEQUE)
        )

        last_cached_list = [
            result for result in last_cached_deque if self.get_user_result(result.result_id, result.user_id)
        ]

        return last_cached_list

    def _add_to_last_cached_deque(self, user_id: int, result_id: int):
        last_cached_results = self._get_last_cached_results()
        last_cached_results.append(
            LastUserCachedResults(user_id=user_id, result_id=result_id)
        )
        cache.set('last_cached_results', last_cached_results)
