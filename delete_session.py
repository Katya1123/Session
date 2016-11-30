from adapter import Adapter
from redis_adapter import RedisAdapter
from file_adapter import FileAdapter


class DeleteSession(Adapter):
    """Удаление сессий пользователя"""

    def delete_session(self, limit=10, file_name='cleaned_session.csv'):
        """Удаление сессий
        :param limit: лимит сессий пользователя
        :param file_name: имя файла куда записать результат"""

        self.delete_session_by_userid(limit, file_name)


if __name__ == '__main__':
    redis = RedisAdapter(host='localhost', port=6379)
    DeleteSession(redis).delete_session(100, 'output_redis.csv')
    file_csv = FileAdapter(file_path=r'session.csv')
    DeleteSession(file_csv).delete_session(100, 'output_csv.csv')
    file_txt = FileAdapter(file_path=r'session.txt')
    DeleteSession(file_txt).delete_session(100, 'output_csv.txt')
