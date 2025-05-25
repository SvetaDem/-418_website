import unittest
from datetime import datetime
import re
from articles_app import is_valid_date

class TestDateValidation(unittest.TestCase):
    def test_valid_dates(self):
        """Корректные случаи для проверки формата даты DD.MM.YYYY"""
        test_cases = [
            {
                'date_str': '01.01.2025',
                'expected': True,
                'description': 'Начало года, валидная дата'
            },
            {
                'date_str': '31.12.2024',
                'expected': True,
                'description': 'Конец года, валидная дата'
            },
            {
                'date_str': '29.02.2024',
                'expected': True,
                'description': 'Високосный год, 29 февраля'
            },
            {
                'date_str': '15.06.2023',
                'expected': True,
                'description': 'Обычная дата в середине года'
            },
            {
                'date_str': '01.03.2000',
                'expected': True,
                'description': 'Дата в прошлом веке'
            }
        ]

        for case in test_cases:
            with self.subTest(msg=case['description']):
                result = is_valid_date(case['date_str'])
                self.assertEqual(result, case['expected'], f"Failed for {case['date_str']}")

    def test_invalid_dates(self):
        """Некорректные случаи для проверки формата даты DD.MM.YYYY"""
        test_cases = [
            {
                'date_str': '32.01.2025',
                'expected': False,
                'description': 'Невалидный день (32)'
            },
            {
                'date_str': '29.02.2023',
                'expected': False,
                'description': '29 февраля в невисокосный год'
            },
            {
                'date_str': '1.1.2025',
                'expected': False,
                'description': 'Неверный формат (однозначные день и месяц)'
            },
            {
                'date_str': '01/01/2025',
                'expected': False,
                'description': 'Неверный разделитель (слэш вместо точки)'
            },
            {
                'date_str': '2025.01.01',
                'expected': False,
                'description': 'Неверный формат (YYYY.MM.DD)'
            },
            {
                'date_str': 'ab.cd.efgh',
                'expected': False,
                'description': 'Буквы вместо цифр'
            },
            {
                'date_str': '01.13.2025',
                'expected': False,
                'description': 'Невалидный месяц (13)'
            },
            {
                'date_str': '00.01.2025',
                'expected': False,
                'description': 'Невалидный день (00)'
            },
            {
                'date_str': '01.00.2025',
                'expected': False,
                'description': 'Невалидный месяц (00)'
            },
            {
                'date_str': '01.01.25',
                'expected': False,
                'description': 'Неверный формат года (две цифры)'
            }
        ]

        for case in test_cases:
            with self.subTest(msg=case['description']):
                result = is_valid_date(case['date_str'])
                self.assertEqual(result, case['expected'], f"Failed for {case['date_str']}")

if __name__ == '__main__':
    unittest.main(verbosity=3)