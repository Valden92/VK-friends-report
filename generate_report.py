import json
import csv
import os


class FileSaver:
    """Генерирует отчет из получаемых данных."""

    def __init__(self, path, parameters, file_format, users_per_page=500):

        self.path_to_save = path
        self.file_name = 'report'
        self.file_format = file_format
        self.users_per_page = users_per_page
        self.fields = parameters

        self.success_mkdir = self.__generate_filepath()

        if self.success_mkdir:
            self.complete_path = self.__filename_concat()

    def __generate_filepath(self):
        """Генерирует конечную папку для сохранения, если это требуется."""
        path = os.getcwd()
        if self.path_to_save == path:
            print('Отчет будет сохранен тут: ', path)
            return True
        else:
            if not os.path.isdir(self.path_to_save):
                try:
                    os.mkdir(self.path_to_save)
                except Exception as e:
                    print(e)
                    return False
                else:
                    print('Новый путь к файлу успешно сформирован.')
                    return True
            else:
                print()

    def __filename_concat(self):
        """Подготавливает конечный путь к файлу дря работы с ним."""
        filename = self.file_name + '.' + self.file_format
        if self.path_to_save == os.path:
            return filename
        else:
            return os.path.join(self.path_to_save, filename)

    @staticmethod
    def save_in_json(file, data, pages=0):
        """Сохраняет отчет в json."""
        if pages:
            paginator = {pages: data}
            file.write(json.dumps(paginator, indent=4, ensure_ascii=False))
        else:
            file.write(json.dumps(data, indent=4, ensure_ascii=False))

    def save_in_csv_or_tsv(self, writer, data, pages=1):
        """Сохраняет отчет в csv или tsv"""
        if pages == 1:
            writer.writeheader()

        writer.writerows(data)

    def run(self, total_user, user_per_page, get_from_api, item_constract):
        users_count = total_user
        with open(self.complete_path, 'w', encoding='utf-8') as file:
            if users_count > user_per_page:
                offset = 0
                page = 1

                if self.file_format == 'json':
                    file.write('[')
                while users_count > 0:
                    items = item_constract.get_items(get_from_api.get_data(count=self.users_per_page,
                                                                           offset=offset))
                    if self.file_format == 'json':
                        self.save_in_json(file, items, pages=page)

                    elif self.file_format == 'csv':
                        writer = csv.DictWriter(file, fieldnames=self.fields, delimiter=',')
                        self.save_in_csv_or_tsv(writer, items, pages=page)

                    elif self.file_format == 'tsv':
                        writer = csv.DictWriter(file, fieldnames=self.fields, delimiter='\t')
                        self.save_in_csv_or_tsv(writer, items, pages=page)

                    page += 1
                    users_count -= user_per_page
                    offset += user_per_page

                    if self.file_format == 'json' and users_count > 0:
                        file.write(',\n')

                if self.file_format == 'json':
                    file.write(']')
            else:
                items = item_constract.get_items(get_from_api.get_data(count=self.users_per_page,
                                                                       offset=0))
                if self.file_format == 'json':
                    self.save_in_json(file, items)

                elif self.file_format == 'csv':
                    writer = csv.DictWriter(file, fieldnames=self.fields, delimiter=',')
                    self.save_in_csv_or_tsv(writer, items)

                elif self.file_format == 'tsv':
                    writer = csv.DictWriter(file, fieldnames=self.fields, delimiter='\t')
                    self.save_in_csv_or_tsv(writer, items)



if __name__ == '__main__':

    FileSaver('D:/git/VK-friends-report/asdsdas42dgvsdf')
    print(os.getcwd())