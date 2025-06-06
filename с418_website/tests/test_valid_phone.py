import unittest
from forms.valid_phone import is_valid_phone

class Test_valid_phone(unittest.TestCase):
    # Проверка невалидных номеров
    def test_invalid_phones(self):
         list_phones_uncor = [
            "", # пустая строка
            "+7", # только начало номера
            "+7(943)", # только начало номера и оператор
            "+79432150012", # нет скобок и тире
            "+7(943)2150012", # нет тире
            "+7943215-00-12", # нет скобок
            "+7(943)215-50-12-2", # количество тире больше положенного
            "+7-943-215-00-12", # тире вместо скобок
            "7(943)215-00-12", # номер без '+'
            "8(943)215-00-12", # начинается с 8
            "+7(943)215 00 12", # есть скобки, но вместо тире - пробелы
            "+7 943 215 00 12", # везде пробелы
            "+7(9430)215-00-12", # в скобках символов больше положенного
            "+7(90)215-00-12", # в скобках символов меньше положенного
            "+7(943)215-00-122", # некорректное количество символов в конце
            "+7(943)215-0-12", # некорректное количество символов после скобок в середине
            "+7(943)21-00-12", # некорректное количество символов после скобок в начале
            "+7(943)215_00_12", # нижнее подчеркиваие вместо тире
            "+71(943)215-00-12", # недопустимое количество символов в начале
            "+7(xxx)xxx-xx-xx", # буквы вместо цифр
            "+7 (943) 215 - 00 - 12", # формат верный, но все написано через пробел
            "+7(943215-00-12", # пропущена скобка
        ]
         for phone in list_phones_uncor:
             self.assertFalse(is_valid_phone(phone), f"Должен быть невалидный: {phone}")

    # Проверка валидных номеров        
    def test_valid_phones(self):
        list_phones_cor = [
            "+7(911)178-20-10",
            "+7(921)343-71-10",
            "+7(500)040-70-12",
            "+7(999)106-97-01",
            "+7(000)111-22-33",
            "+7(880)946-65-90",
            "+7(966)773-75-42",
            "+7(103)025-05-25",
            "+7(950)105-55-05",
            "+7(102)404-44-33",
            "+7(581)489-10-17",
            "+7(789)117-01-13",
            "+7(990)456-87-53",
            "+7(903)147-58-07",
            "+7(505)005-01-02",
        ]
        for phone in list_phones_cor:
            self.assertTrue(is_valid_phone(phone), f"Должен быть валидный: {phone}")

if __name__ == '__main__':
    unittest.main()
