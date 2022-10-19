from django.core.cache import caches
from django_redis.cache import RedisCache


class ResultCacheHandler:
    """
    Класс для взаимодействия с кешем и добавления/удаления/получения
    данных результатов из него.
    """

    @classmethod
    def get_handler(cls, cache_db_name: str = 'default'):
        """
        Создает и возвращает сущность класса. Принимает название базы
        данных, что будет использоваться для хранения результатов.
        """
        return cls(cache_db_name)

    def clean_cache(self):
        """Удаляет все данные из кеша."""
        self.cache_db.clear()

    def get_result(self, result_id: int, user_id: int):
        """Возвращает данные из кеша."""
        return self.cache_db.get(f'result:{result_id}', version=user_id)

    def add_result(self, data, user_id: int) -> int:
        """Добавляет данные в кеш. Возвращает id результата."""
        result_id = self.increment_current_result_id(user_id)
        self.cache_db.set(f'result:{result_id}', data, version=user_id)
        return result_id

    def delete_result(self, result_id: int, user_id: int) -> bool:
        """Удаляет данные из кеша."""
        return self.cache_db.delete(f'result:{result_id}', version=user_id)

    def get_current_result_id(self, user_id: int):
        """Возвращает значение `results_id` из кеша."""
        return self.cache_db.get('last_result_id', version=user_id)

    def delete_current_result_id(self, user_id: int):
        self.cache_db.delete('last_result_id', version=user_id)

    def increment_current_result_id(self, user_id: int) -> int:
        """
        Увеличивает значение `results_id` на 1. Если `results_id` ещё нет
        в кеше, то добавляет его.
        """
        if not self.get_current_result_id(user_id):
            self.set_current_result_id(0, user_id)
        return self.cache_db.incr('last_result_id', version=user_id)

    def get_results_keynames(self, user_id: int) -> list[str | None]:
        """Возвращает все ключи данных из кэша, если таковы есть."""
        current_id = self.get_current_result_id(user_id)
        if not current_id:
            return []
        result_key_names = []
        for result_id in range(current_id, 0, -1):
            if not self.get_result(result_id, user_id):
                break
            result_key_names.append(f'result:{result_id}')
        return result_key_names

    @property
    def cache_db(self) -> RedisCache:
        """Возвращает сущность, над которой выполняются операции."""
        return caches[self.cache_db_name]

    def set_current_result_id(self, new_result_id: int, user_id: int):
        """
        Добавляет значение `result_id` в кеш. Значение не может
        быть меньше 0.
        """
        if new_result_id < 0:
            raise ValueError("`new_result_id` не может быть меньше нуля.")
        self.cache_db.set('last_result_id', new_result_id, version=user_id)

    def __init__(self, cache_db_name: str):
        self.cache_db_name = cache_db_name
