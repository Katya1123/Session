class AbstractAdapter:
    """Абстрактный класс для адаптера"""

    @staticmethod
    def parse_session(session):
        """Парсит сессию
        :param session: сессия"""

        return str(session).split('-')
