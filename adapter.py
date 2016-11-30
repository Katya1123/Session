from abstract_adapter import AbstractAdapter


class Adapter(AbstractAdapter):
    """Базовый класс для адаптера"""

    _source = None

    def __init__(self, source):
        """
        :param source: ресурс
        """

        self._source = source

    def parse_data(self):
        """
        Составляем словарь с частотой встречаемости id пользователей
        :return: словарь вида {'0053bf97': 3, '0052956b': 2, '0056b6c4': 8, '00566bb3': 1}
        """

        ids = {}

        try:
            for session in self._source.unpack:
                id_client, id_user, way_of_auth, random_path = self.parse_session(session)
                ids[id_user] = 1 if id_user not in ids.keys() else ids[id_user] + 1
        except Exception as e:
            print("Произошли ошибки: {}".format(e))

        return ids

    def delete_session_by_userid(self, limit, file_name):
        """
        Получим файл с удаленными сессиями пользователей
        :param limit: количество сессий для хранения
        :param file_name: имя выходного файла
        """

        if limit < 0:
            raise Exception("Число должно быть не отрицательно")
        ids = self.parse_data()
        # получили список идентификаторов пользователей для удаления
        ids_for_delete = {i: ids[i] >= limit for i in ids.keys()}
        self._source.change(ids_for_delete, file_name)
