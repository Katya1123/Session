import os
from abstract_adapter import AbstractAdapter


class FileAdapter(AbstractAdapter):
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

    @property
    def unpack(self):
        """
        Распакованные данные из хранилища
        :return: Распакованные данные из хранилища
        """

        return open(self._file_path)

    def change(self, ids_for_delete, file_name):
        """
        Получим файл с удаленными сессиями пользователей
        :param ids_for_delete: словарь вида
        :param file_name: имя выходного файла
        """

        path = os.path.dirname(self._file_path)
        output_file_path = os.path.join(path, file_name)
        output_file = open(output_file_path, "w")
        file = open(self._file_path)

        try:
            for session in file:
                id_client, id_user, way_of_auth, random_path = self.parse_session(session)
                if not ids_for_delete[id_user]:
                    output_file.write(session)
            print("Файл с удаленными сессиями {}".format(output_file_path))
        except Exception as e:
            print("Произошли ошибки: {}".format(e))
        finally:
            output_file.close()
            file.close()
