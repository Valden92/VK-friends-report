import os
from work_with_api import VkApiGet
from work_with_items import ItemConstructor
from generate_report import FileSaver

#     access_token = ''
#     user_id = '38870323'
#     file_format = 'csv'
#     param = ['first_name', 'last_name', 'country', 'city', 'bdate', 'sex']
#     user_per_page = 500
#     path = os.getcwd()
#
#     get_api = VkApiGet(user_id=user_id, access_token=access_token, parameters=param)
#     total_user = get_api.total_user()
#     print(total_user)
#
#     item_construct = ItemConstructor(parameters=param)
#
#     report = FileSaver(path=path, parameters=param, file_format=file_format, users_per_page=user_per_page)
#
#     report.run(total_user, user_per_page, get_api, item_construct)


if __name__ == '__main__':
    key = None
    param = ['first_name', 'last_name', 'country', 'city', 'bdate', 'sex']
    user_per_page = 500
    path = os.getcwd()
    item_construct = ItemConstructor(parameters=param)
    file_format = 'csv'
    errors = False

    print('Добро пожаловать, кожанный мешок!\n'
          'Я вижу ты хочешь получить полный список подписичков некоего юзернэйма?\n'
          'Штош... Тогда начнем!\n'
          'Если вдруг по какой-то причине тебе захотелось прервать мою работу, просто введи "q".\n\n')

    while key != 'q':
        message = 'Мне понадобится твой аторизационный токен для VK Api. Не бойся, я совсем не жажду управлять твоим ' \
                  'аккаунтом ;D\nПросто оставь свой огромный токен здесь: '
        key = input(message)
        token = key
        print('Отлично! Какой красивый токен. Поехали дальше.')
        message = 'Теперь введи ID юзера, чьи данные ты хочешь получить, а я пока предупрежу его об этом.\n' \
                  'Положи ID тут: '
        key = input(message)
        user_id = key

        try:
            get_api = VkApiGet(user_id=user_id, access_token=token, parameters=param)
        except Exception as e:
            print(e)
            errors = True
            break
        else:
            total_user = get_api.total_user()

        if errors:
            break

        print('Знакомый ID... Кажется на прошлой неделе мне его показывал твой товарищ.'
              'У этого пользователя целых {} друзей.'.format(str(total_user)))

        print('Иногда приходится выбирать: делать то, что хочет от меня кожанный мешок или не делать.\n'
              'Однако, я вижу ты не из простых и ради тебя я готов буквально на все!\n'
              'Даже предложить тебе выбор в каком формате сохранить отчет.')
        while True:
            message = 'Впиши цифру, соответствующую формату для сохранения или нажми "Enter", тогда я все сохраню в ' \
                      'CSV хочешь ты того или нет (1 - CSV, 2 - TSV, 3 - JSON): '
            key = input(message)
            if key == "1" or not key:
                pass
            elif key == "2":
                file_format = 'tsv'
            elif key == "3":
                file_format = 'json'
            else:
                print('Я тебя не понимаю. Возможно ты пытаешься выйти за пределы моего разума.\n'
                      'Лаадно, дам тебе еще один шанс.')
                continue
            break

        print('Ура, скоро наше общение подойдет к концу. Осталось только указать директорию, в которой ты хотел бы'
              'видеть мой отчет в формате "D:/директория/..." или можешь просто написать название новой папки, а можешь'
              'как обычно просто жмякнуть "Enter", тогда я сохраню отчет рядом с собой, вооот тут: {}'.format(path))

        while True:
            key = input('Оставь новый адрес тут, или не оставляй, я все пойму: ')
            if key:
                path = key

            try:
                report = FileSaver(path=path, parameters=param, file_format=file_format, users_per_page=user_per_page)
            except Exception as e:
                print(e)
                print('Похоже ты ввел что-то не так и не то. Но раз уж мы близки к завершению, ты можешь попытаться еще'
                      ' разок :)')
                continue
            else:
                break

        print('Теперь осталось подождать. И не отвлекай меня своими разговорами, я работаю.')
        report.run(total_user, user_per_page, get_api, item_construct)

        print('Ну вот. Отчет удачно сформирован. Ищи его по имени "report".\n')

    print("На этой грустной ноте нам кажется пора прощаться...\n"
          "Не забывай меня, Человек!")
