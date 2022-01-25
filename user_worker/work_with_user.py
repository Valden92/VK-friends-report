import os
import sys
from api_worker.work_with_api import VkApiGet
from generate_report.generate_report import FileSaver


param = ['first_name', 'last_name', 'country', 'city', 'bdate', 'sex']
user_per_page = 500


def run_program():
    """Запуск программы VK Api parser."""

    print("Добро пожаловать в VK-api parser.\n"
          "Если захотите прервать выполнение программы, введите 'Q'.")

    # Будет спрашивать авторизационный токен и ID пока пользователь не введет корректный или не выйдет из программы.
    while True:
        token = input('Введите аторизационный токен для VK-api: ').strip()
        if_q_exit(token)

        user_id = input('Введите ID пользователя для извлечения данных: ').strip()
        if_q_exit(user_id)

        # Тут проверяет токен и ID на правильность, а так же проверяет возможность получения данных из VK api.
        try:
            get_api, total_user = run_vk_api(user_id, token, param)
        except ValueError:
            continue
        except (ConnectionError, TypeError):
            break

        # Выводит общеее найденное количество подписчиков для ID.
        if total_user > 0:
            print('Для ID: {} обнаружено {} пользователей.\n'.format(user_id, total_user))
        else:
            no_users(user_id)

        # Запрашивает у пользователя формат отчета.
        file_format = input_format()
        print('Файл будет сохранен в {} формате.\n'.format(file_format.upper()))

        # Запрашивает у пользователя путь для сохранения отчета.
        report = input_path(file_format)

        print('\nВсе необходимые данные получены. Извлечение данных запущено.\n'
              'Ожидайте результатов...')

        # Запускает извлечение данных.
        try:
            report.run(total_user=total_user, get_from_api=get_api)
        except Exception as e:
            print(e)
            break
        else:
            print('\nДанные успешно извлечены. Отчет с именем "report.{}" сгенерирован.'.format(file_format))
            break

    print('Работа с программой завершена.')


def run_vk_api(user_id, token, parameters):
    """Создает экземпляр класса VkApiGet и проверят наличие ошибок в вводе данных, а так же соединение с Vk api
    и наличие ошибок в ответе Vk api.
    :param user_id: ID пользователя, по которому делается запрос с целью извлечения его подписчиков;
    :param token: ваш токен (токен приложения) с которого выполняется запрос к VK api;
    :param parameters: параметры для передачи их в поле fields VK api, формирующие конечным список данных
    об одном пользователе.
    :except ValueError: если введены значения, содержащие неверный тип или сами по себе неверного типа;
    :except ConnectionError: если наблюдаются проблемы с соединением VK api или наличие ошибок в ответе и т.д.
    :return: экземпляр класса VkApiGet и общее количество пользователей для запрошенного ID.
    """
    try:
        api = VkApiGet(user_id=user_id, access_token=token, parameters=parameters)
    except ValueError as e:
        print(e)
        raise ValueError
    except ConnectionError as e:
        print(e)
        raise ConnectionError
    else:
        return api, api.users_count


def no_users(user_id):
    """Работает, если у ID не обнаружено подписчиков.
    Предлагает либо начать заново вводить все данные, для нового запроса, либо завершить работу с программой.
    :param user_id: ID пользователя, по которому делается запрос с целью извлечения его подписчиков.
    """
    print('Для ID:{} подписчиков не обнаружено.'.format(user_id))
    while True:
        key = input("Желаете начать заново (Y) или прекратить выполнение программы (Q): ").strip().lower()
        if_q_exit(key)
        if key == 'y':
            break
        else:
            print('Введенное значение не распознано. Попробуйте еще раз.')
            continue


def if_q_exit(string):
    """Завершает работу приложения, если передаваемый параметр равен 'Q'.
    :param string: параметр типа str.
    """
    if string.lower() == 'q':
        sys.exit()


def input_format():
    """Получает формат отчета для сохранения от пользователя.
    :return: формат отчета в виде строки ('csv', 'tsv', 'json').
    """
    msg = 'Впишите цифру, соответствующую формату (1 - CSV, 2 - TSV, 3 - JSON) для сохранения отчета или ' \
          'нажми "Enter", тогда автоматически будет выбран CSV формат: '
    while True:
        key = input(msg).strip().lower()
        if_q_exit(key)
        if key == "1" or not key:
            return 'csv'
        elif key == "2":
            return 'tsv'
        elif key == "3":
            return 'json'
        else:
            print('Введенное значение не распознано. Попробуйте еще раз.')
            continue


def input_path(file_format):
    """Запрашивает у пользователя путь для сохранения отчета и создает экземпляр FileSaver.
    :param file_format: формат отчета в виде строки ('csv', 'tsv', 'json').
    :except (SyntaxError, FileNotFoundError): выбрасывает, если указан невозможный путь для сохранения.
    :return: экземпляр FileSaver.
    """
    msg = 'Введите путь для сохранения отчета в виде (C:/Users/...) или напишите название новой директории.\n' \
          'Если такой директории не сущестует, то программа попытается ее создать.\n' \
          'Также вы можете просто нажать "Enter" и файл сохранится в одной директории с программой.'
    print(msg)
    while True:
        path = input('Укажите путь для сохранения отчета: ').strip()
        if_q_exit(path)

        if not path:
            path = os.getcwd()

        try:
            report = FileSaver(path=path, parameters=param, file_format=file_format, users_per_page=user_per_page)
        except (SyntaxError, FileNotFoundError, OSError) as e:
            print(e)
            print('Пробуйте ввести путь еще раз или введите "Q" для завершения программы.')
            continue
        else:
            return report


if __name__ == '__main__':
    run_program()
