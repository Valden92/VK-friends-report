from datetime import datetime


class ItemConstructor:
    """Позволяет получить реформатировать список подсписчиков, извлеченный из VK api.
    """

    def __init__(self, parameters):
        """Инициализация атрибутов.

        :param parameters: параметры для получения готовой структуры словаря для одного юзера.
        """
        self.parameters = parameters

    def get_items(self, items):
        """Получение списка подписчиков."""
        format_items = []
        for user in items:
            if 'deactivated' in user.keys() and user['first_name'] == 'DELETED':
                pass
            else:
                format_items.append(self.get_one_item(user))
        return format_items

    def get_one_item(self, user):
        """Полчение реформатированного словаря по переданным параметрам для одного юзера.

        :param user: исходный dict, извлеченный из api vk.
        """
        one_user = {}

        for param in self.parameters:
            try:
                if param == 'city' or param == 'country':
                    one_user[param] = user[param]['title']
                elif param == 'bdate':
                    one_user[param] = self.__date_to_iso(user[param])
                elif param == 'sex':
                    if user[param] == 1:
                        one_user[param] = 'Женский'
                    elif user[param] == 2:
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
        try:
            date_obj = datetime.strptime(date, '%d.%m.%Y')
        except ValueError:
            date_obj = datetime.strptime(date, '%d.%m')
            return date_obj.strftime("%m-%d")

        return date_obj.strftime("%Y-%m-%d")
