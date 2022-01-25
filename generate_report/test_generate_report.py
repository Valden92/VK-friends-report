from unittest import TestCase
import unittest
import os
from generate_report import FileSaver


class FileSaverTest(TestCase):

    def setUp(self):
        """Входные данные."""
        self.file_format = 'csv'
        self.param = ['first_name', 'last_name', 'country', 'city', 'bdate', 'sex']
        self.this_dir = os.getcwd()
        self.rep_dir = os.path.join(self.this_dir, 'REPORTS')
        self.another_dir = os.path.join(self.this_dir, 'new_dir')
        self.another_dir_2 = os.path.join(self.this_dir, 'new_dir', 'new_dir')

    def test_generate_filepath(self):
        """Проверяет работу генератора директории."""
        self.assertEqual(FileSaver(self.this_dir, self.param, self.file_format).path_to_save, self.rep_dir)
        os.rmdir(self.rep_dir)

        self.assertEqual(FileSaver('new_dir', self.param, self.file_format).path_to_save, self.another_dir)
        os.rmdir(self.another_dir)

        with self.assertRaises(FileNotFoundError):
            FileSaver('Z:/NotUsers/Пользователь/Desktop', self.param, self.file_format)
            FileSaver('new_dir/new_dir', self.param, self.file_format)

        with self.assertRaises(OSError):
            FileSaver('CD:\\Users\\Пользователь\\Desktop', self.param, self.file_format)
            FileSaver('\*&reports', self.param, self.file_format)
            FileSaver('CD:/Users/Пользователь/Desktop', self.param, self.file_format)

    def test_filename_join(self):
        """Проверяет правильность получения конечного адреса файла."""
        path = os.path.join(self.rep_dir, 'report.{}'.format(self.file_format))
        self.assertEqual(FileSaver(self.this_dir, self.param, self.file_format).complete_path, path)

        path = os.path.join(self.another_dir, 'report.{}'.format(self.file_format))
        self.assertEqual(FileSaver(self.another_dir, self.param, self.file_format).complete_path, path)


unittest.main()
