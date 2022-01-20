import requests
from generate_url import *


def connection_checker(request, url):
    """Проверка статуса соединения и наличия ошибок при получении ответа на запрос.

    :param request - объект запроса, полученный из сессии;
    :param url - сформированный адрес для запроса к api.
    """
    r = request.get(url)
    if not r.status_code == requests.codes.ok:
        r.raise_for_status()

    if 'error' in r.json().keys():
        print('ERROR')


def total_user(request, url):
    """Получает по закпросу к api общее количество друзей пользователя.

    :param request - объект запроса, полученный из сессии;
    :param url - сформированный адрес для запроса к api.
    """
    count = int(request.get(url).json()['response']['count'])
    return count


def get_one_item(user):
    """Собирает словарь по параметрам для одного извелченного пользователя."""
    parameters = ['first_name', 'last_name' , 'country', 'city', 'bdate', 'sex']


access_token = '665c80434de0aa5cca1621f670f54264d984a5b2a9f0706b46cd4b20358964946912495f05f2ae2464306'
u_id = '38870323'
url = get_url(u_id, access_token, count=0, offset=1)


session = requests.Session()
connection_checker(session, url)
user_count = total_user(session, url)
print(user_count)

if user_count == 0:
    print('Друзей в списке не найдено')
elif user_count > 500:
    count = 500
    page = 0
    while user_count > 0:

        url = get_url(u_id, access_token, count=count, offset=count)
        dataset = session.get(url).json()['response']['items']

        with open('vk_friends_report.json', 'w') as file:
            for user in dataset:
                get_one_item(user)



        user_count -= 500
else:
    pass
