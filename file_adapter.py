import os


class FileAdapter:
    """Разбор данных сессии из файла. На вход подается *.txt, *.csv"""

    _file_path = None

    def __init__(self, file_path):
        """
        :param file_path: путь к файлу
        """

        self._file_path = file_path
        if os.path.exists(self._file_path):
            print("Файл {} существует".format(self._file_path))
        else:
            raise Exception("Файл {} не существует".format(self._file_path))

    def parsed_data(self):
        """
        Составляем словарь с частотой встречаемости id пользователей
        :return: словарь вида {'0053bf97': 3, '0052956b': 2, '0056b6c4': 8, '00566bb3': 1}
        """

        ids = {}

        file = open(self._file_path)
        try:
            for session in file:
                id_client, id_user, way_of_auth, random_path = session.split('-')
                if id_user in ids.keys():
                    ids[id_user] += 1
                else:
                    ids[id_user] = 1
        except Exception as e:
            print("Произошли ошибки: {}".format(e))
        finally:
            file.close()

        return ids

    def delete_session_by_userid(self, ids_for_delete, file_name):
        """
        Получим файл с удаленными сессиями пользователей
        """

        path = os.path.dirname(self._file_path)
        output_file_path = os.path.join(path, file_name)
        output_file = open(output_file_path, "w")
        file = open(self._file_path)

        try:
            for session in file:
                id_client, id_user, way_of_auth, random_path = session.split('-')
                if id_user not in ids_for_delete:
                    output_file.write(session)
                else:
                    pass
            print("Файл с удаленными сессиями {}".format(output_file_path))
        except Exception as e:
            print("Произошли ошибки: {}".format(e))
        finally:
            output_file.close()
            file.close()
