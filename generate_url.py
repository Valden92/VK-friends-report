import urllib.parse


def value_checker(user_id, token, api_version, count, offset):
    """Проверка значений для сборки url

    :param user_id: id пользователя по которому будет производится сбор списка друзей;
    :param token: access token приложения с которого будет выполняться запрос;
    :param api_version: версия VK api (по умолчанию 5.131);
    :param count: количество пользователей о которых нужно получить информацию;
    :param offset: смещение для получения подмножества списка друзей.
    """

    errors = ''

    if not user_id.isdigit():
        errors += "Передаваемый user_id должен содержать только числовые значения.\n"

    if not str(count).isdigit() or not str(offset).isdigit():
        errors += "Число пользователей и смещение должны быть целыми положительными числами.\n"

    if token.isdigit():
        errors += "Токен не может быть числом.\n"

    try:
        float(api_version)
    except ValueError:
        errors += "Версия api должна быть числом.\n"

    if errors:
        raise ValueError(errors)


def get_url(user_id, token, api_version='5.131', count=0, offset=0):
    """Собирает URL для запроса к VK-api.

    :param user_id: id пользователя по которому будет производится сбор списка друзей;
    :param token: access token приложения с которого будет выполняться запрос;
    :param api_version: версия VK api (по умолчанию 5.131);
    :param count: количество пользователей о которых нужно получить информацию;
    :param offset: смещение для получения подмножества списка друзей.
    """
    value_checker(user_id, token, api_version, count, offset)

    # Метод для запроса списка друзей
    method_name = 'friends.get'

    # Параметры метода. Для поля fields перечислены дополнительные аргументы.
    params = {'user_id': user_id,
              'order': 'name',
              'count': count,
              'offset': offset,
              'fields': 'first_name,last_name,country,city,bdate,sex',
              'name_case': 'nom'}

    return 'https://api.vk.com/method/{}?{}&access_token={}&v={}'.format(method_name,
                                                                         urllib.parse.urlencode(params),
                                                                         token, api_version)


if __name__ == '__main__':
    access_token = '665c80434de0aa5cca1621f670f54264d984a5b2a9f0706b46cd4b20358964946912495f05f2ae2464306'
    u_id = '38870323'

    url = get_url(u_id, access_token, offset=10)
    print(url)