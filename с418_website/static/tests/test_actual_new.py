import unittest
from actual_new_logic import is_valid_date  # Импорт из твоего файла с логикой

class TestIsValidDate(unittest.TestCase):
    def test_valid_dates(self):
        """Корректные случаи: формат и существование даты DD.MM.YYYY"""
        valid_dates = [
            ('01.01.2025', 'Начало года'),
            ('31.12.2030', 'Конец года в будущем'),
            ('29.02.2024', 'Високосный год'),
            ('15.06.2025', 'Обычная дата'),
            ('01.03.2000', 'Валидная прошлая дата'),
        ]
        for date_str, description in valid_dates:
            with self.subTest(description=description):
                self.assertTrue(is_valid_date(date_str), f"Должно быть валидным: {date_str}")

    def test_invalid_dates(self):
        """Некорректные случаи: неправильный формат или несуществующие даты"""
        invalid_dates = [
            ('32.01.2025', 'Невалидный день (32)'),
            ('29.02.2023', 'Не високосный год'),
            ('1.1.2025', 'Неполный формат'),
            ('01/01/2025', 'Неправильный разделитель'),
            ('2025.01.01', 'Формат YYYY.MM.DD'),
            ('ab.cd.efgh', 'Буквы вместо цифр'),
            ('01.13.2025', 'Месяц 13'),
            ('00.01.2025', 'День 00'),
            ('01.00.2025', 'Месяц 00'),
            ('01.01.25', 'Двузначный год'),
            ('', 'Пустая строка'),
            ('01-01-2025', 'Дефис вместо точки'),
        ]
        for date_str, description in invalid_dates:
            with self.subTest(description=description):
                self.assertFalse(is_valid_date(date_str), f"Должно быть невалидным: {date_str}")

if __name__ == '__main__':
    unittest.main(verbosity=2)