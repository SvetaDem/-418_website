import unittest
from partners_form import validate_phone, validate_date, validate_email

class TestValidation(unittest.TestCase):
    def test_validate_phone(self):
        """Tests phone number validation (+XXXXXXXXXXXX format)."""
        # Test valid phone numbers
        valid_phones = ["+71234567890", "+19876543210"]
        for phone in valid_phones:
            with self.subTest(phone=phone):
                is_valid, msg = validate_phone(phone)
                self.assertTrue(is_valid, f"Valid phone {phone} should pass")
                self.assertEqual(msg, "", f"Message should be empty for {phone}")

        # Test invalid phone numbers
        invalid_phones = [
            "+1-123-456-7890",  # Old format
            "+123456789",       # Too short
            "+1234567890123",   # Too long
            "+a1234567890",     # Non-numeric
            "123456789012"      # Missing +
        ]
        for phone in invalid_phones:
            with self.subTest(phone=phone):
                is_valid, msg = validate_phone(phone)
                self.assertFalse(is_valid, f"Invalid phone {phone} should fail")
                self.assertNotEqual(msg, "", f"Error message should be present for {phone}")

    def test_validate_date(self):
        """Tests date validation (DD-MM-YYYY format)."""
        # Test valid dates
        valid_dates = ["01-05-2025", "02-06-2025"]
        for date in valid_dates:
            with self.subTest(date=date):
                is_valid, msg = validate_date(date)
                self.assertTrue(is_valid, f"Valid date {date} should pass")
                self.assertEqual(msg, "", f"Message should be empty for {date}")

        # Test invalid dates
        invalid_dates = [
            "03-06-2025",       # Future date (today is 02-06-2025)
            "32-05-2025",       # Invalid day
            "01-13-2025",       # Invalid month
            "2025-05-01",       # Wrong format (YYYY-MM-DD)
            "01/05/2025",       # Wrong separator
            "01-05-2025 12:00"  # Extra time
        ]
        for date in invalid_dates:
            with self.subTest(date=date):
                is_valid, msg = validate_date(date)
                self.assertFalse(is_valid, f"Invalid date {date} should fail")
                self.assertNotEqual(msg, "", f"Error message should be present for {date}")

    def test_validate_email(self):
        """Tests email validation (no IP addresses in domain)."""
        # Test valid emails
        valid_emails = [
            "user@example.com",
            "test.email@domain.co.uk",
            "valid+email@subdomain.com"
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                is_valid, msg = validate_email(email)
                self.assertTrue(is_valid, f"Valid email {email} should pass")
                self.assertEqual(msg, "", f"Message should be empty for {email}")

        # Test invalid emails
        invalid_emails = [
            "user@[192.168.1.1]",  # IP address not allowed
            "user@domain",         # Missing TLD
            "user@.com",           # Invalid domain
            ".user@domain.com",    # Starts with dot
            "user..name@domain.com",  # Consecutive dots
            "a" * 65 + "@domain.com"  # Local part too long
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                is_valid, msg = validate_email(email)
                self.assertFalse(is_valid, f"Invalid email {email} should fail")
                self.assertNotEqual(msg, "", f"Error message should be present for {email}")

if __name__ == '__main__':
    unittest.main()