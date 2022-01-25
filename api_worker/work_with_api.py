import requests


class VkApiGet:
    """Работает с VK api."""

    def __init__(self, user_id, access_token, parameters):
        """Инициализация параметров.
        :param user_id: ID пользователя, по которому делается запрос с целью извлечения его подписчиков;
        :param access_token: ваш токен (токен приложения) с которого выполняется запрос к VK api;
        :param parameters: параметры для передачи их в поле fields VK api, формирующие конечным список данных
        об одном пользователе.
        """
        self.user_id = user_id
        self.token = access_token
        self.fields = ','.join(parameters)

        # Дополнительные параметры запроса к api:  версия VK api, метод запроса, url адрес запроса.
        self.api_version = '5.131'
        self.method = 'friends.get'
        self.url = 'https://api.vk.com/method/{}?'.format(self.method)

        # Проверка на корректность передаваемых данных
        self.__check_values()

        # Если данные корректны, то заполняется dict с параметрами запроса, передаваемый в requests.
        self.parameters = {'user_id': self.user_id,
                           'order': 'name',
                           'count': '0',
                           'offset': '0',
                           'fields': self.fields,
                           'name_case': 'nom',
                           'access_token': self.token,
                           'v': self.api_version}

        # Проверка удачного соединения с api и наличия ошибок в получаемом запросе, которые возможны при
        # некорректном access_token, user_id и т.д.
        self.__connect = True
        self.__check_access()

        if self.__connect:
            # Общее количество пользователей в подписчиках.
            self.users_count = self.__total_user()

    def __check_values(self):
        """Проверка передаваемых значений.
        :except ValueError: выбрасывает исключение при несоответствии данных определенному виду или типу.
        """
        # Сообщение, передаваемое в исключение.
        errors = ''

        if not self.user_id.isdigit():
            errors += "Передаваемый user_id должен содержать только числовые значения.\n"

        # Токен - комбинация буквенных и цифровых символов.
        if self.token.isdigit() or not self.token.isalnum() or self.token.isalpha() or not self.token.isascii():
            errors += "Токен содержит недопустимые символы. Он должен состоять из комбинации символов ASCII и цифр.\n"

        try:
            float(self.api_version)
        except ValueError:
            errors += "Версия api должна быть числом.\n"

        if errors:
            raise ValueError(errors)

    def __check_access(self):
        """Проверка статуса соединения и наличия ошибок при получении ответа на запрос.
        :except ConnectionError: выбрасывает исключение, если отсутствует соединение или данные получены с ошибками.
        """
        try:
            r = requests.get(self.url, params=self.parameters)
        except requests.exceptions.ConnectionError:
            self.__connect = False
            raise ConnectionError('Ошибка соединения. Установить соединение не удалось.')

        # Сообщение, которое либо передастся в исключение, либо выведется на экран, если все удачно.
        text = ''

        if not r.status_code == requests.codes.ok:
            self.__connect = False
            text += 'Неудачное соединение с VK api: ' + str(r.status_code) + '\n'
        else:
            text += 'Соединение с VK api установлено. Статус: OK\n'

        if 'error' in r.json().keys():
            # Получает причину наличия ошибки из VK api.
            text += r.json()['error']['error_msg']
            self.__connect = False

        if not self.__connect:
            raise ConnectionError(text)
        else:
            print(text)

    def __total_user(self):
        """Получает по закпросу к api общее количество друзей пользователя.
        :return: общее количество друзей для запрошенного id.
        :except ConnectionError: выбрасывает исключение, если проверка на соединение c VK api прошла неудачно.
        """
        if self.__connect:
            # При count=0 и offset=1 извлекается пустой список пользователей.
            self.parameters['count'] = '0'
            self.parameters['offset'] = '1'
            return int(requests.get(self.url, params=self.parameters).json()['response']['count'])
        else:
            msg = "Соединение отсутствует c VK api. Данные о количестве пользователей недоступны."
            raise requests.exceptions.ConnectionError(msg)

    def get_data(self, count=0, offset=0):
        """Получает список пользователей с параметрами в виде dict.
        :param count: количество пользователей, которое требуется получить в одном запросе;
        :param offset: смещение внутри массива пользователей.
        :except ConnectionError: выбрасывает исключение, если проверка на соединение c VK api прошла неудачно.
        """
        if self.__connect:
            # В запрос передаются только параметры типа str!
            self.parameters['count'] = str(count)
            self.parameters['offset'] = str(offset)
            return requests.get(self.url, params=self.parameters).json()['response']['items']
        else:
            msg = "Соединение отсутствует c VK api. Данные о пользователях недоступны."
            raise requests.exceptions.ConnectionError(msg)


if __name__ == '__main__':
    u_id = '38870323'
    token = ''
    param = ['first_name', 'last_name', 'country', 'city', 'bdate', 'sex']
    get_api = VkApiGet(user_id=u_id, access_token=token, parameters=param)

    data = get_api.get_data(count=10, offset=2000)
    print(data)
