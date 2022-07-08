from collections import deque
from datetime import datetime

from django.core.cache import caches

from common.utils import is_args_type
from config import settings
from trainer.utils.datastructures import (
    UserTypingResult,
    ResultFieldType,
    LastUserCachedResults,
    UserTypingResultWithUser
)


class ResultCache:
    """
    Класс для взаимодействия с кешем и добавления/удаления/получения
    данных из него.
    """

    cache_base_name = 'default'

    @property
    def result_cache(self):
        if not self.cache_base_name:
            raise ValueError("Укажите атрибут `cache_base_name`.")
        if not isinstance(self.cache_base_name, str):
            raise ValueError(f"`cache_base_name` должен быть типа `str`, а не {type(self.cache_base_name)}.")

        cache = caches[self.cache_base_name]

        return cache

    def get_user_result(self, result_id: int, user_id: int):
        """Возвращает данные из кеша."""
        if not is_args_type(int, result_id, user_id):
            raise ValueError("`get_user_result` принимает аргументы только типа `int`.")

        return self.result_cache.get(f'result:{result_id}', version=user_id)

    def set_user_result(self, data, user_id: int):
        """Добавляет данные в кеш."""
        if not is_args_type(int, user_id):
            raise ValueError("`user_id` должны быть только типа `int`.")

        result_id = self.increment_current_result_id(user_id)
        self.result_cache.set(f'result:{result_id}', data, version=user_id)

    def delete_user_result(self, result_id: int, user_id: int) -> bool:
        """Удаляет данные из кеша."""
        if not is_args_type(int, result_id, user_id):
            raise ValueError("`delete_user_result` принимает аргументы только типа `int`.")

        return self.result_cache.delete(f'result:{result_id}', version=user_id)

    def get_user_current_result_id(self, user_id: int):
        """Возвращает значение `results_id` из кеша."""
        if not is_args_type(int, user_id):
            raise ValueError("`get_user_current_result_id` принимает аргументы только типа `int`.")

        return self.result_cache.get('last_result_id', version=user_id)

    def delete_user_current_result_id(self, user_id: int):
        if not is_args_type(int, user_id):
            raise ValueError("`delete_user_current_result_id` принимает аргументы только типа `int`.")

        self.result_cache.delete('last_result_id', version=user_id)

    def _set_user_current_result_id(self, new_result_id: int, user_id: int):
        """
        Добавляет значение `results_id` в кеш. Значение не может
        быть меньше 0.
        """
        if not is_args_type(int, new_result_id, user_id):
            raise ValueError("`set_user_current_result_id` принимает аргументы только типа `int`.")
        if new_result_id < 0:
            raise ValueError("`new_result_id` не может быть меньше нуля.")

        self.result_cache.set('last_result_id', new_result_id, version=user_id)

    def increment_current_result_id(self, user_id: int) -> int:
        """
        Увеличивает значение `results_id` на 1. Если `results_id` ещё нет
        в кеше, то добавляет его.
        """
        if not is_args_type(int, user_id):
            raise ValueError("`increment_current_result_id` принимает аргументы только типа `int`.")
        if not self.get_user_current_result_id(user_id):
            self._set_user_current_result_id(0, user_id)

        return self.result_cache.incr('last_result_id', version=user_id)

    def get_results_keynames(self, user_id: int) -> list[str | None]:
        """Возвращает все ключи данных из кэша, если таковы есть."""
        if not is_args_type(int, user_id):
            raise ValueError("`get_results_keynames` принимает аргументы только типа `int`.")

        current_id = self.get_user_current_result_id(user_id)

        if not current_id:
            return []

        result_key_names = []
        for result_id in range(current_id, 0, -1):
            if not self.get_user_result(result_id, user_id):
                break
            result_key_names.append(f'result:{result_id}')

        return result_key_names


class CurrentUserCache(ResultCache):
    """
    Класс для взаимодействия с кешем данных определенного пользователя,
    который определяется по атрибуту `user_id`.
    """

    user_id: int = None

    @property
    def current_user_result_id(self) -> int | None:
        """
        Возвращает текущий `id` ключа результата. Если такого
        ещё нет, возвращает `None`.
        """
        return self.get_user_current_result_id(self.user_id)

    def increment_current_user_result_id(self) -> int:
        """Увеличивает текущее значение `current_user_result_id` на один."""
        return self.increment_current_result_id(self.user_id)

    def get_current_user_results_keynames(self) -> list[str | None]:
        """Возвращает все существующую ключи данных из кеша."""
        return self.get_results_keynames(self.user_id)

    def get_current_user_result(self, result_id: int):
        """
        Возвращает данные результата по ключу `result_id`. Если
        их нет, вернет `None`.
        """
        return self.get_user_result(result_id, self.user_id)

    def set_current_user_result(self, data):
        """Добавляет в кеш данные результата пользователя."""
        self.set_user_result(data, self.user_id)

    def get_all_current_user_results(self):
        """
        Возвращает все записи результатов пользователя. Если таких ещё нет,
        вернет пустой список.
        """
        result_keynames = self.get_current_user_results_keynames()
        results: dict = self.result_cache.get_many(
            result_keynames, version=self.user_id
        )
        return [result for result in results.values()]

    def delete_current_user_results(self) -> int:
        """
        Очищает все данные результатов пользователя из кэша
        и возвращает количество удаленных ключей.
        """
        result_keynames = self.get_current_user_results_keynames()
        if result_keynames:
            self.result_cache.delete_many(result_keynames, version=self.user_id)
        self.delete_user_current_result_id(self.user_id)
        return len(result_keynames)


class TrainerResultCache(CurrentUserCache):
    """
    Миксин для работы с кешем данных результатов тренажера определенного
    пользователя.
    """

    def cache_result_data(self, data: UserTypingResult) -> None:
        """Кеширует результат определенного пользователя."""
        self.set_current_user_result(data)

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


class AllUserResultsMixin(ResultCache):
    """
    Миксин для хранения и получения последних данных результатов из кеша.
    Максимальное количество сохраненных объектов в очереди определяется
    константой `MAX_LENGTH_LAST_CACHED_DEQUE`, что задаётся в файле конфигурации.
    """

    user_model = None

    def add_to_last_cached_results(self, user_id, result_id):
        """
        Сохраняет данные о результате с полями `user_id` и `result_id`.
        """
        last_cached_results = self._get_last_cached_results()
        last_cached_results.append(
            LastUserCachedResults(user_id=user_id, result_id=result_id)
        )
        self.result_cache.set('last_cached_results', last_cached_results)

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

    def get_user_model(self):
        return self.user_model

    def get_last_cached_results_with_users(self, amount: int) -> list[UserTypingResultWithUser]:
        """
        Возвращает все последние записи результатов из кеша с их пользователями.

        Длина может быть меньше, так как данные результатов могли исчезнуть
        из кеша.
        """
        last_results_data: list[tuple] = []
        users_pk_list: list[int] = []

        for result in self._get_last_cached_results(amount):
            result_from_cache: UserTypingResult = self.get_user_result(result.result_id, result.user_id)
            if result_from_cache:
                last_results_data.append(
                    (result_from_cache, result.user_id)
                )
                users_pk_list.append(result.user_id)

        if not users_pk_list:
            return []

        users_instance = self.get_user_model().filter(pk__in=users_pk_list)
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

    def get_raw_last_cached_results(self, amount: int) -> list[UserTypingResult]:
        """
        Возвращает список, длиной `amount` или меньше, последних данных
        результатов из кеша.

        Длина может быть меньше, так как данные результатов могут исчезнуть
        из кеша.
        """
        last_results_data: list[UserTypingResult] = []

        for result in self._get_last_cached_results(amount):
            result_from_cache: UserTypingResult = self.get_user_result(result.result_id, result.user_id)
            if result_from_cache:
                last_results_data.append(result_from_cache)

        return last_results_data

    def _get_last_cached_results(self, amount=settings.MAX_LENGTH_LAST_CACHED_DEQUE) -> list[LastUserCachedResults]:
        """Возвращает очередь с `LastUserCachedResults` из кеша."""
        last_cached_deque: deque[LastUserCachedResults] = self.result_cache.get(
            'last_cached_results',
            deque(maxlen=settings.MAX_LENGTH_LAST_CACHED_DEQUE)
        )

        last_cached_list = [
                               result for result in last_cached_deque
                               if self.get_user_result(result.result_id, result.user_id)
                           ][:amount]

        return last_cached_list
