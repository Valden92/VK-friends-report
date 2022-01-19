import urllib.parse


def get_url(user_id, token, api_version='5.131', offset=0):
    """Собирает URL для запроса к VK-api.

    :param user_id - id пользователя по которому будет производится сбор списка друзей;
    :param token - access token приложения с которого будет выполняться запрос;
    :param api_version - версия VK api (по умолчанию 5.131);
    :param offset - смещение для получения подмножества списка друзей.
    """
    # Метод для запроса списка друзей
    method_name = 'friends.get'

    # Параметры метода. Для поля fields перечислены дополнительные аргументы.
    params = {'user_id': user_id,
              'order': 'name',
              # 'count': 10,
              'offset': offset,
              'fields': 'first_name,last_name,country,city,bdate,sex',
              'name_case': 'nom'}

    return 'https://api.vk.com/method/{}?{}&access_token={}&v={}'.format(method_name,
                                                                         urllib.parse.urlencode(params),
                                                                         token, api_version)


if __name__ == '__main__':
    access_token = ''
    u_id = ''

    url = get_url(u_id, access_token)
    print(url)
