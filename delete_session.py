from adapter_from_file import AdapterFromFile
from adapter_from_redis import AdapterFromRedis


class DeleteSession:
    """Удаление сессий пользователя"""

    _adapter = None

    def __init__(self, adapter):
        """
        Инициализация данных
        :param adapter: ресурс с данными
        """

        self._adapter = adapter

    def delete_session(self, limit=10, file_name='cleaned_session.csv'):
        """Удаление сессий
        :param limit: лимит сессий пользователя
        :param file_name: имя файла куда записать результат"""

        if limit < 0:
            raise Exception("Число должно быть не отрицательно")
        ids = self._adapter.parsed_data()
        # получили список идентификаторов пользователей для удаления
        ids_for_delete = [i for i in ids.keys() if ids[i] >= limit]
        self._adapter.delete_session_by_userid(ids_for_delete, file_name)


if __name__ == '__main__':
    redis = AdapterFromRedis(host='localhost', port=6379)
    DeleteSession(redis).delete_session(100, 'output_redis.csv')
    file_csv = AdapterFromFile(file_path=r'session.csv')
    DeleteSession(file_csv).delete_session(100, 'output_csv.csv')
    file_txt = AdapterFromFile(file_path=r'session.txt')
    DeleteSession(file_txt).delete_session(100, 'output_csv.txt')
