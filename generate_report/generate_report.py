import json
import csv
import os
from item_parser.item_parser import ItemConstructor


class FileSaver:
    """Генерирует отчет из получаемых данных."""

    def __init__(self, path, parameters, file_format, users_per_page=500):
        """Инициализация атрибутов.
        :param path: путь для сохранения отчета;
        :param parameters: параметры, требуемые для генерации headers в CSV и TSV форматах и парсинга данных;
        :param file_format: формат сохранения данных (csv, tsv, json);
        :param users_per_page: ограничение количества пользователей в одном запросе (по умолчанию 500).
        """

        self.path_to_save = path
        self.file_format = file_format
        self.users_per_page = users_per_page
        self.fields = parameters

        # Имя отчета по умолчанию.
        self.file_name = 'report'

        # Проверка наличия готового пути для сохранения или попытка содать указанный путь.
        self.success_mkdir = True
        self.__generate_filepath()

        if self.success_mkdir:
            # Если директория для сохранения получена удачно, получаем готовый путь для сохранения.
            self.complete_path = self.__filename_join()

    def __generate_filepath(self):
        """Генерирует конечную папку для сохранения, если это требуется."""

        # Проверка, является ли указанная директория исходной (для программы).
        if self.path_to_save == os.getcwd():
            self.path_to_save = os.path.join(self.path_to_save, 'REPORTS')
            if not os.path.isdir(self.path_to_save):
                os.mkdir(self.path_to_save)
            print('Отчет будет сохранен тут: ', self.path_to_save)
            self.success_mkdir = True
        else:

            # Проверяет существует ли указанная директория, если нет, то попытается ее создать.
            if not os.path.isdir(self.path_to_save):
                try:
                    os.mkdir(self.path_to_save)
                except SyntaxError:
                    self.success_mkdir = False
                    raise SyntaxError('Путь для сохранения указан неверно.')
                except FileNotFoundError:
                    self.success_mkdir = False
                    raise FileNotFoundError('Системе не удается найти указанный путь.')
                except OSError:
                    self.success_mkdir = False
                    raise OSError('Синатксическая ошибка в имени файла или папке.')
                else:
                    self.path_to_save = os.path.abspath(self.path_to_save)
                    print('Новый путь к файлу успешно сформирован.\n'
                          'Отчет будет сохранен тут: ', self.path_to_save)
                    self.success_mkdir = True
            else:
                self.path_to_save = os.path.abspath(self.path_to_save)
                print('Отчет будет сохранен тут: ', self.path_to_save)
                self.success_mkdir = True

    def __filename_join(self):
        """Подготавливает конечный путь к файлу для работы с ним."""
        filename = self.file_name + '.' + self.file_format

        # Если путь к файлу является исходным (для программы), то в дальнейшем достаточно просто названия файла
        # с расширением, если нет, то преобразует в новый путь для сохранения файла.
        if self.path_to_save == os.path:
            return filename
        else:
            return os.path.join(self.path_to_save, filename)

    @staticmethod
    def __save_in_json(file, data, in_while, page=1):
        """Сохраняет отчет в json.
        :param file: открытый файл для сохранения;
        :param data: данные для сохранения;
        :param in_while: переменная типа bool для обозначения запущено ли сохранение в цикле;
        :param page: номер страницы.
        """
        if in_while:
            # Если данных слишком много, они разбиваются на подмассивы и прикрепляются к страницам.
            paginator = {page: data}
            file.write(json.dumps(paginator, indent=4, ensure_ascii=False))
        else:
            file.write(json.dumps(data, indent=4, ensure_ascii=False))

    @staticmethod
    def __save_in_csv_or_tsv(writer, data, in_while, page=1):
        """Сохраняет отчет в csv или tsv
        :param writer: экзмепляр DictWriter;
        :param data: данные для сохранения;
        :param in_while: переменная типа bool для обозначения запущено ли сохранение в цикле;
        :param page: номер страницы.
        """
        if not in_while or page == 1:
            # Пишем названия столбцов в файл один раз.
            writer.writeheader()
        writer.writerows(data)

    def __file_saver(self, file, item_construct, get_from_api, page=0, in_while=False, offset=0):
        """Извлекает подмассив пользователей и отправляет их сохраняться в нужном формате.
        :param file: открытый файл для сохранения;
        :param item_construct: экземпляр класса ItemConstructor для предобработки переданного массива данных;
        :param get_from_api: экземпляр класса VkApiGet для получения подмассива данных из VK api;
        :param page: номер страницы;
        :param in_while: переменная типа bool для обозначения запущено ли сохранение в цикле;
        :param offset: смещение внутри массива пользователей.
        """
        items = item_construct.get_items(get_from_api.get_data(count=self.users_per_page,
                                                               offset=offset))
        if self.file_format == 'json':
            self.__save_in_json(file, items, in_while, page=page)

        elif self.file_format == 'csv' or self.file_format == 'tsv':
            delimiter = ','
            if self.file_format == 'tsv':
                delimiter = '\t'

            writer = csv.DictWriter(file, fieldnames=self.fields, delimiter=delimiter)
            self.__save_in_csv_or_tsv(writer, items, in_while, page=page)

    def run(self, total_user, get_from_api):
        """Запуск получения и сохранения данных в файл.
        :param total_user: общее количество пользователей у переданного ID.
        :param get_from_api: экземпляр класса VkApiGet для получения подмассива данных из VK api.
        :except EmptyValueError: выбрасывается в случае, когда известно, что по переданному ID отсутствуют подписчики.
        """
        users_count = total_user
        if users_count == 0:
            raise EmptyValueError

        with open(self.complete_path, 'w', encoding='utf-8') as file:
            item_construct = ItemConstructor(parameters=self.fields)
            if users_count > self.users_per_page:
                offset = 0
                page = 1
                in_while = True

                # В этом месте идет отдельная запись скобки перед обходом данных для json формата.
                # Иначе формат записи внутри файла будет неверный.
                if self.file_format == 'json':
                    file.write('[')
                print('Записано пользователей:')
                while users_count > 0:
                    self.__file_saver(file, item_construct, get_from_api, page=page, in_while=in_while, offset=offset)
                    print('\t- ', item_construct.users_counter)
                    page += 1
                    users_count -= self.users_per_page
                    offset += self.users_per_page

                    # Точно так же для json. Т.к. dicts внутри должны быть разделены запятой, причем для последней
                    # записи запятая в конце не ставится.
                    if self.file_format == 'json' and users_count > 0:
                        file.write(',\n')

                # В конце для json записывается закрывающая скобка.
                if self.file_format == 'json':
                    file.write(']')
            else:
                self.__file_saver(file, item_construct, get_from_api)
                print('Записано пользователей: ', item_construct.users_counter)

            print('Деактивированных пользователей (не записанных): ', item_construct.deactivate_users)


class EmptyValueError(Exception):
    """Исключение в случае отсутствия значений."""

    def __str__(self):
        return 'Значений для обработки не найдено.'
