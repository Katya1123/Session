import redis
from abstract_adapter import AbstractAdapter


class RedisAdapter(AbstractAdapter):
    """Разбор данных сессии из редиса"""

    _redis_connect = None
    _pipe = None

    def __init__(self, host, port=6395):
        """
        :param host: хост для подключения к редису
        :param port: порт для подключения к редису
        """

        try:
            self._redis_connect = redis.Redis(host=host, port=port)
            self._pipe = self._redis_connect.pipeline()
        except Exception as e:
            print("Не установлено подключение к редису {}:{}. Причина {}".format(host, port, e))

    @property
    def unpack(self):
        """
        Распакованные данные из хранилища
        :return: Распакованные данные из хранилища
        """

        return self._redis_connect.scan_iter()

    def change(self, ids_for_delete, file_name):
        """
        Получим файл с удаленными сессиями пользователей
        :param ids_for_delete: словарь вида
        :param file_name: имя выходного файла
        """

        try:
            for session in self._redis_connect.scan_iter():
                id_client, id_user, way_of_auth, random_path = self.parse_session(session)
                if ids_for_delete[id_user]:
                    self._pipe.delete(session)
            self._pipe.execute()
            print("Удалили сессии из редиса")
            self.get_data(file_name)
        except Exception as e:
            print("Произошли ошибки: {}".format(e))

    def get_data(self, file_name):
        """Получить данные с редиса в текстовом виде
        :param file_name: имя файла куда записать"""

        output_file = open(file_name, "w")
        try:
            for key in self._redis_connect.scan_iter():
                output_file.write(str(key))
                output_file.write('\n')
            print('Записали данные из редиса в файл {}'.format(file_name))
        except Exception as e:
            print("Произошли ошибки: {}".format(e))
        finally:
            output_file.close()
