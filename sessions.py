import csv
import requests
import json
from datetime import datetime
from generate_url import *


def connection_checker(url):
    """Проверка статуса соединения и наличия ошибок при получении ответа на запрос.

    :param url: сформированный адрес для запроса к api.
    :return connect: bool наличие удачного соединения и получения данных.
    """
    r = requests.get(url)
    connect = True
    text = ''

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


def total_user(url):
    """Получает по закпросу к api общее количество друзей пользователя.

    :param url: сформированный адрес для запроса к api.
    :return count: общее количество друзей для запрошенного id.
    """
    count = int(requests.get(url).json()['response']['count'])
    return count


def date_to_iso(date):
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


def get_one_item(user):
    """Собирает словарь по параметрам для одного извелченного пользователя.

    :param user: исходный словарь, извлеченный из api vk.
    :return one_user: пересобранный словарь с ключами: ['first_name', 'last_name', 'country', 'city', 'bdate', 'sex'].
    """
    parameters = ['first_name', 'last_name', 'country', 'city', 'bdate', 'sex']
    one_user = {}

    for param in parameters:
        try:
            if param == 'city' or param == 'country':
                one_user[param] = user[param]['title']
            elif param == 'bdate':
                one_user[param] = date_to_iso(user[param])
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


def to_item_list(user_id, token, users_per_page, offset=0):
    """Генерирует список для записи.

    :param user_id: id пользователя по которому будет производится сбор списка друзей;
    :param token: access token приложения с которого будет выполняться запрос;
    :param users_per_page: количество аккаунтов, получаемое в одном запросе;
    :param offset: смещение для получения подмножества списка друзей.
    :return items: список, состоящий из dicts c описанием пользователей.
    """
    url = get_url(user_id, token, count=users_per_page, offset=offset)
    data = requests.get(url).json()['response']['items']
    items = []
    for user in data:
        if 'deactivated' in user.keys() and user['first_name'] == 'DELETED':
            pass
        else:
            items.append(get_one_item(user))
    return items


if __name__ == '__main__':

    access_token = ''
    u_id = '38870323'
    url = get_url(u_id, access_token, count=0, offset=1)

    connection = connection_checker(url)

    if connection:
        user_count = total_user(url)
        print(user_count)
        count = 500
        offset = 0
        parameters = ['first_name', 'last_name', 'country', 'city', 'bdate', 'sex']

        if user_count == 0:
            print('Друзей в списке не найдено.')

        else:
            f_format = 'csv'
            with open('report.{}'.format(f_format), 'w', encoding='utf-8') as file:
                if f_format == 'json':
                    if user_count > count:
                        page = 1
                        file.write('[')
                        while user_count > 0:
                            paginator = {page: to_item_list(u_id, access_token, count, offset=offset)}
                            file.write(json.dumps(paginator, indent=4, ensure_ascii=False))
                            page += 1
                            user_count -= count
                            offset += count
                            if user_count > 0:
                                file.write(',\n')
                            print(user_count)
                        file.write(']')

                    else:
                        file.write(json.dumps(to_item_list(u_id, access_token, count), indent=4, ensure_ascii=False))

                elif f_format == 'csv' or f_format == 'tsv':
                    if f_format == 'csv':
                        delimiter = ','
                    elif f_format == 'tsv':
                        delimiter = '\t'

                    writer = csv.DictWriter(file, fieldnames=parameters, delimiter=delimiter)
                    writer.writeheader()
                    if user_count > count:
                        while user_count > 0:
                            writer.writerows(to_item_list(u_id, access_token, count, offset=offset))
                            user_count -= count
                            offset += count
                    else:
                        writer.writerows(to_item_list(u_id, access_token, count))
