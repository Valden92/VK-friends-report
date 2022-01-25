from unittest import TestCase
import unittest
from item_parser import ItemConstructor


class ItemConstructorTest(TestCase):

    def setUp(self):
        """Входные данные."""
        self.param = ['first_name', 'last_name', 'country', 'city', 'bdate', 'sex']

        self.dates = [['1.10.1992', '1992-10-01'],
                      ['13.2.2012', '2012-02-13'],
                      ['1.1.2001', '2001-01-01'],
                      ['12.11.1987', '1987-11-12'],
                      ['1.2', '02-01'],
                      ['10.2', '02-10'],
                      ['2.11', '11-02'],
                      ['12.11', '11-12']]

        self.source_users = [{"id": 492882314,
                              "first_name": "Алексей",
                              "last_name": "Трофимов",
                              "can_access_closed": "true",
                              "is_closed": "false",
                              "sex": 2,
                              "bdate": "20.9.1990",
                              "city": {"id": 668, "title": "Серов"},
                              "country": {"title": "Россия", "id": 1},
                              "track_code": "c4f12c17TH2zJZnatLdOms0LpK"},
                             {"first_name": "Akshay",
                              "last_name": "Трофимова",
                              "sex": 1,
                              "bdate": "20.9",
                              "city": {"id": 668, "title": "Томск"},
                              "country": {"title": "Россия", "id": 1}},
                             {"first_name": "Алексей",
                              "last_name": "Трофимов"},
                             {"deactivated": "deleted",
                              "first_name": "DELETED",
                              "last_name": "",
                              "sex": 1,
                              "track_code": "a566d551qdpPnF6h11QsZ"}]

        self.final_users = [{"first_name": "Алексей",
                             "last_name": "Трофимов",
                             "country": "Россия",
                             "city": "Серов",
                             "bdate": "1990-09-20",
                             "sex": "Мужской"},
                            {"first_name": "Akshay",
                             "last_name": "Трофимова",
                             "city": "Томск",
                             "country": "Россия",
                             "bdate": "09-20",
                             "sex": "Женский"},
                            {"first_name": "Алексей",
                             "last_name": "Трофимов",
                             "country": None,
                             "city": None,
                             "bdate": None,
                             "sex": None}]

    def test_date_to_iso(self):
        """Проверка метода преобразования даты."""
        item_construct = ItemConstructor(self.param)
        for date in self.dates:
            self.assertEqual(item_construct._date_to_iso(date[0]), date[1])

    def test_get_one_item(self):
        """Проверка метода извлечения нужных данных для одного юзера."""
        item_construct = ItemConstructor(self.param)
        for i in range(len(self.source_users)):
            if i < 3:
                self.assertEqual(item_construct.get_one_item(self.source_users[i]), self.final_users[i])

    def test_get_items(self):
        """Проверка метода обхода списка с данными юзеров."""
        item_construct = ItemConstructor(self.param)
        self.assertEqual(item_construct.get_items(self.source_users), self.final_users)

    def test_counter(self):
        """Проверка счетчика извлеченных и пропущенных юзеров."""
        item_construct = ItemConstructor(self.param)
        item_construct.get_items(self.source_users)
        self.assertEqual(item_construct.users_counter, 3)
        self.assertEqual(item_construct.deactivate_users, 1)


unittest.main()
