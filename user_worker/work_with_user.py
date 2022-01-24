import os
import requests
from api_worker.work_with_api import VkApiGet
from generate_report.generate_report import FileSaver

param = ['first_name', 'last_name', 'country', 'city', 'bdate', 'sex']
user_per_page = 500


def run_program():
    """Запуск программы VK Api parser."""

    print("Добро пожаловать в VK-api parser.\n"
          "Если захотите прервать выполнение программы, введите 'Q'.")

    while True:
        token = input('Введите аторизационный токен для VK-api: ').strip()
        if token.lower() == 'q':
            break

        user_id = input('Введите ID пользователя для извлечения данных: ').strip()
        if user_id.lower() == 'q':
            break

        try:
            get_api, total_user = run_vk_api(user_id, token, param)
        except ValueError:
            continue
        except (ConnectionError, TypeError):
            break

        if total_user > 0:
            print('Для ID: {} обнаружено {} пользователей.\n'.format(user_id, total_user))
        else:
            key = no_users()
            if key == 'q':
                break

        file_format = input_format()
        if file_format == 'q':
            break
        else:
            print('Файл будет сохранен в {} формате.\n'.format(file_format.upper()))

        report = input_path(file_format)
        if report == 'q':
            break

        print('\nВсе необходимые данные получены. Извлечение данных запущено.\n'
              'Ожидайте результатов...')

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
    try:
        api = VkApiGet(user_id=user_id, access_token=token, parameters=parameters)
    except ValueError as e:
        print(e)
        raise ValueError
    except ConnectionError as e:
        print(e)
        raise ConnectionError
    except requests.exceptions.ConnectionError:
        print('Ошибка соединения. Установить соединение не удалось.')
        raise ConnectionError
    else:
        return api, api.users_count


def no_users():
    print('Для ID:{} подписчиков не обнаружено.')
    while True:
        key = input("Желаете начать заново (Y) или прекратить выполнение программы (Q): ").strip().lower()
        if key == 'y' or key == 'q':
            return key
        else:
            print('Введенное значение не распознано. Попробуйте еще раз.')
            continue


def input_format():
    msg = 'Впишите цифру, соответствующую формату (1 - CSV, 2 - TSV, 3 - JSON) для сохранения отчета или ' \
          'нажми "Enter", тогда автоматически будет выбран CSV формат: '
    while True:
        key = input(msg).strip().lower()
        if key == "1" or not key:
            return 'csv'
        elif key == "2":
            return 'tsv'
        elif key == "3":
            return 'json'
        elif key == 'q':
            return 'q'
        else:
            print('Введенное значение не распознано. Попробуйте еще раз.')
            continue


def input_path(file_format):
    msg = 'Введите путь для сохранения отчета или напишите название новой директории.\n' \
          'Если такой директории не сущестует, то программа попытается ее создать.\n' \
          'Также вы можете просто нажать "Enter" и файл сохранится в одной директории с программой.'
    print(msg)
    while True:
        path = input('Укажите путь для сохранения отчета: ').strip()
        if path.lower() == 'q':
            return path.lower()
        else:
            if not path:
                path = os.getcwd()

            try:
                report = FileSaver(path=path, parameters=param, file_format=file_format, users_per_page=user_per_page)
            except Exception as e:
                print(e)
                print('Пробуйте ввести путь еще раз или введите "Q" для завершения программы.')
                continue
            else:
                return report


if __name__ == '__main__':
    run_program()
