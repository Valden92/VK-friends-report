from datetime import datetime


class ItemConstructor:
    """Позволяет получить реформатировать список подсписчиков, извлеченный из VK api.
    """

    def __init__(self, parameters):
        """Инициализация атрибутов.

        :param parameters: параметры для получения готовой структуры словаря для одного юзера.
        """
        self.parameters = parameters
        self.female = 1
        self.male = 2

    def get_items(self, items):
        """Получение списка подписчиков.

        :param items: массив, содержащий dicts с данными о пользователях, полученными из VK api.
        :return: форматированный список, содержащий dicts с данными о пользователях, согласно переданными параметрам.
        """
        format_items = []
        for user in items:
            # Фильтрация деактивированных пользователей с отсутствием каких-либо полезных данных.
            if 'deactivated' in user.keys() and user['first_name'] == 'DELETED':
                pass
            else:
                format_items.append(self.get_one_item(user))
        return format_items

    def get_one_item(self, user):
        """Полчение реформатированного словаря по переданным параметрам для одного юзера.

        :param user: исходный dict, извлеченный из api vk.
        :return: dict, содержащий данные об одном пользователе в соответствии с переданными параметрами.
        """
        one_user = {}

        for param in self.parameters:
            # Некоторых данных может не быть, для этого используется try-except.
            try:
                if param == 'city' or param == 'country':
                    one_user[param] = user[param]['title']
                elif param == 'bdate':
                    one_user[param] = self.__date_to_iso(user[param])
                elif param == 'sex':
                    if user[param] == self.female:
                        one_user[param] = 'Женский'
                    elif user[param] == self.male:
                        one_user[param] = 'Мужской'
                else:
                    one_user[param] = user[param]
            except KeyError:
                one_user[param] = None

        return one_user

    @staticmethod
    def __date_to_iso(date):
        """Переводит полученную дату в iso формат YYYY-MM-DD.

        :param date: дата в формате 'DD.MM.YYYY' или 'DD.MM'.
        :return: дата в формате ISO 'YYYY-MM-DD' или 'MM-DD'.
        """
        # Некоторые пользователи скрывают свой год рождения или не заполняют его.
        # В таком случае остается только месяц и день.
        try:
            date_obj = datetime.strptime(date, '%d.%m.%Y')
        except ValueError:
            date_obj = datetime.strptime(date, '%d.%m')
            return date_obj.strftime("%m-%d")

        return date_obj.strftime("%Y-%m-%d")
