from collections import deque

from django.db.models import QuerySet

from account.models import User
from config import settings
from type_results.cache_handler import ResultCacheHandler
from type_results.structs import UserTypingResult


class CurrentUserResults:
    """
    Класс для взаимодействия с кешем данных определенного пользователя,
    который определяется по атрибуту `user_id`.
    """

    def increment_user_result_id(self) -> int:
        """Увеличивает текущее значение `current_user_result_id` на один."""
        return self.cache_handler.increment_current_result_id(self.user_id)

    def get_user_result(self, result_id: int):
        """
        Возвращает данные результата по ключу `result_id`. Если
        их нет, вернет `None`.
        """
        return self.cache_handler.get_result(result_id, self.user_id)

    def add_user_result(self, data: UserTypingResult):
        """Добавляет в кеш данные результата пользователя."""
        return self.cache_handler.add_result(vars(data), self.user_id)

    def get_all_user_results(self):
        """
        Возвращает все записи результатов пользователя. Если таких ещё нет,
        вернет пустой список.
        """
        results = self.cache_handler.cache_db.get_many(
            self.user_results_keynames, version=self.user_id
        )
        return [result for result in results.values()][::-1]

    def delete_all_user_results(self) -> int:
        """
        Очищает все данные результатов пользователя из кэша
        и возвращает количество удаленных ключей.
        """
        if result_keynames := self.user_results_keynames:
            self.cache_handler.cache_db.delete_many(result_keynames, version=self.user_id)
        self.cache_handler.delete_current_result_id(self.user_id)
        return len(result_keynames)

    @property
    def user_current_result_id(self) -> int | None:
        """
        Возвращает текущий `id` ключа результата. Если такого
        ещё нет, возвращает `None`.
        """
        return self.cache_handler.get_current_result_id(self.user_id)

    @property
    def user_results_keynames(self) -> list[str | None]:
        """Возвращает все существующую ключи данных из кеша."""
        return self.cache_handler.get_results_keynames(self.user_id)

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.cache_handler = ResultCacheHandler.get_handler()


class AllUserResults:
    """
    Миксин для хранения и получения последних данных результатов из кеша.
    Максимальное количество сохраненных объектов в очереди определяется
    константой `MAX_LENGTH_LAST_CACHED_DEQUE`, что задаётся в файле конфигурации.
    """

    def add_to_cached_results(self, user_id: int, result_id: int):
        """
        Сохраняет данные о результате с полями `user_id` и `result_id`.
        """
        last_cached_results = self.get_last_cached_results_info()
        last_cached_results.appendleft(LastUserCachedResults(user_id=user_id, result_id=result_id))
        self.cache_handler.cache_db.set('last_cached_results', last_cached_results)

    def get_cached_results_with_users(
            self, amount: int, users: QuerySet[User]
    ) -> list[UserTypingResultWithUser | None]:
        """
        Возвращает все последние записи результатов из кеша с их пользователями.
        Длина может быть меньше, так как данные результатов могли исчезнуть
        из кеша.
        """
        if not (results_from_cache := self.get_last_cached_results_info()):
            return []
        last_results_data = []
        users = users.filter(pk__in=[result.user_id for result in results_from_cache])
        for result in results_from_cache:
            result_from_cache = self.cache_handler.get_result(result.result_id, result.user_id)
            user = users.filter(pk=result.user_id)
            if result_from_cache and user.exists():
                last_results_data.append(UserTypingResultWithUser(**result_from_cache, user=user))
        return last_results_data[:amount]

    def get_last_cached_results_info(self) -> deque[LastUserCachedResults | None]:
        """Возвращает очередь с `LastUserCachedResults` из кеша."""
        last_cached_deque = self.cache_handler.cache_db.get(
            'last_cached_results', deque(maxlen=settings.MAX_LENGTH_LAST_CACHED_DEQUE)
        )
        return last_cached_deque

    def __init__(self):
        self.cache_handler = ResultCacheHandler.get_handler()
