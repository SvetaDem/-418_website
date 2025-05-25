import unittest
from partners_form import validate_phone, validate_date

class TestValidation(unittest.TestCase):
    def test_validate_phone(self):
        """Tests phone number validation."""
        # Тест валидных номеров
        valid_phones = ["+1-123-456-7890", "+7-987-654-3210"]
        for phone in valid_phones:
            with self.subTest(phone=phone):
                is_valid, msg = validate_phone(phone)
                self.assertTrue(is_valid, f"Valid phone {phone} should pass")
                self.assertEqual(msg, "", f"Message should be empty for {phone}")

        # Тест невалидных номеров
        invalid_phones = ["123-456-7890", "+1-123-456-789", "+1-123-456-78901", "+a-123-456-7890"]
        for phone in invalid_phones:
            with self.subTest(phone=phone):
                is_valid, msg = validate_phone(phone)
                self.assertFalse(is_valid, f"Invalid phone {phone} should fail")
                self.assertNotEqual(msg, "", f"Error message should be present for {phone}")

    def test_validate_date(self):
        """Tests date validation."""
        # Тест валидных дат
        valid_dates = ["2025-05-01", "2025-05-27"]
        for date in valid_dates:
            with self.subTest(date=date):
                is_valid, msg = validate_date(date)
                self.assertTrue(is_valid, f"Valid date {date} should pass")
                self.assertEqual(msg, "", f"Message should be empty for {date}")

        # Тест невалидных дат
        invalid_dates = ["2025-05-28", "2025-13-01", "2025-05-32", "2025/05/01", "2025-05-27 12:00"]
        for date in invalid_dates:
            with self.subTest(date=date):
                is_valid, msg = validate_date(date)
                self.assertFalse(is_valid, f"Invalid date {date} should fail")
                self.assertNotEqual(msg, "", f"Error message should be present for {date}")

if __name__ == '__main__':
    unittest.main()
