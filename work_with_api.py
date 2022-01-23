import requests


class VkApiGet:
    """Работает с VK api."""

    def __init__(self, user_id, access_token, parameters):
        self.user_id = user_id
        self.token = access_token
        self.api_version = '5.131'
        self.method = 'friends.get'
        self.url = 'https://api.vk.com/method/{}?'.format(self.method)
        self.fields = ','.join(parameters)

        self.__check_values()

        self.parameters = {'user_id': self.user_id,
                           'order': 'name',
                           'count': '0',
                           'offset': '0',
                           'fields': self.fields,
                           'name_case': 'nom',
                           'access_token': self.token,
                           'v': self.api_version}

        self.connect = self.__check_access()

        if self.connect:
            self.users_count = self.total_user()

    def __check_values(self):
        """Проверка передаваемых значений."""
        errors = ''

        if not self.user_id.isdigit():
            errors += "Передаваемый user_id должен содержать только числовые значения.\n"

        if self.token.isdigit():
            errors += "Неверный токен.\n"

        try:
            float(self.api_version)
        except ValueError:
            errors += "Версия api должна быть числом.\n"

        if errors:
            raise ValueError(errors)

    def __check_access(self):
        """Проверка статуса соединения и наличия ошибок при получении ответа на запрос."""
        r = requests.get(self.url, params=self.parameters)
        text = ''
        connect = True

        if not r.status_code == requests.codes.ok:
            connect = False
            text += 'Bad connection: ' + str(r.status_code) + '\n'
        else:
            text += 'Connection: OK\n'

        if 'error' in r.json().keys():
            text += r.json()['error']['error_msg']
            connect = False

        print(text)
        return connect

    def total_user(self):
        """Получает по закпросу к api общее количество друзей пользователя.

        :return: общее количество друзей для запрошенного id.
        """
        if self.connect:
            self.parameters['offset'] = '1'
            return int(requests.get(self.url, params=self.parameters).json()['response']['count'])
        else:
            print("Соединение с VK api установить не удалось.")

    def get_data(self, count=0, offset=0):
        """Получает список пользователей с параметрами в виде dict.

        :param count: количество пользователей, которое требуется получить в одном запросе;
        :param offset: смещение внутри массива пользователей.
        """
        if self.connect:
            self.parameters['count'] = str(count)
            self.parameters['offset'] = str(offset)
            return requests.get(self.url, params=self.parameters).json()['response']['items']
        else:
            print("Соединение с VK api установить не удалось.")


if __name__ == '__main__':
    u_id = '38870323'
    token = ''
    param = ['first_name', 'last_name', 'country', 'city', 'bdate', 'sex']
    get_api = VkApiGet(user_id=u_id, access_token=token, parameters=param)

    data = get_api.get_data(count=10, offset=2000)
    print(data)
