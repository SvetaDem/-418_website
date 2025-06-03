import unittest
from partners_form import validate_phone, validate_date, validate_email, validate_name, validate_description

class TestValidation(unittest.TestCase):
    def test_validate_phone(self):
        """Tests phone number validation (+XXXXXXXXXXXX format)."""

        valid_phones = ["+71234567890", "+19876543210"]
        for phone in valid_phones:
            with self.subTest(phone=phone):
                is_valid, msg = validate_phone(phone)
                self.assertTrue(is_valid, f"Valid phone {phone} should pass")
                self.assertEqual(msg, "", f"Message should be empty for {phone}")


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
        """Tests date validation (DD-MM-YYYY format, not in the future, not before 01-01-2000)."""

        valid_dates = [
            "01-05-2025",
            "17-11-2011",
            "01-01-2000"   # Earliest allowed date
        ]
        for date in valid_dates:
            with self.subTest(date=date):
                is_valid, msg = validate_date(date)
                self.assertTrue(is_valid, f"Valid date {date} should pass")
                self.assertEqual(msg, "", f"Message should be empty for {date}")

        invalid_dates = [
            "03-06-2025",       # Future date (today is 02-06-2025)
            "31-12-1999",       # Before minimum date (01-01-2000)
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
        valid_emails = [
            "user@example.com",
            "test.email@domain.co.uk",
            "user.name@example.com",
            "user123@example.com",
            "user+tag@example.com",
            "user.name@sub.example.com",
            "user@example.co.uk",
            "a@b.cd",
            f"{'a' * 64}@example.com",  # max local part
            f"user@{'sub.' * 50}example.com"
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                is_valid, msg = validate_email(email)
                self.assertTrue(is_valid, f"Valid email {email} should pass")
                self.assertEqual(msg, "", f"Message should be empty for {email}")

        invalid_emails = [
            "user@[192.168.1.1]",   # IP address not allowed
            "",                     # empty string
            "@example.com",         # no local part
            "user@",                # no domen
            "user@.com",            # domen starts with .
            "user@example..com",    # double '.'
            "user@example_com",     # '_' in domen
            "user@example.c",       # one character in part
            "user@-example.com",    # '-' in start of domen
            "user@example.com.",    # '.' in the end
            "user name@example.com", # ' ' in local part
            "user..name@example.com",# double '.' in local part
            "user@.com",            # dot after @
            f"{'a' * 65}@example.com",  # local part 65 characters
            f"user@{'a' * 252}.com"     # domen 256 cherecters
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                is_valid, msg = validate_email(email)
                self.assertFalse(is_valid, f"Invalid email {email} should fail")
                self.assertNotEqual(msg, "", f"Error message should be present for {email}")

    def test_validate_name(self):
        """Tests company name validation (2 to 50 characters)."""
        valid_names = [
            "TechCorp",                 # Short but valid
            "Minecraft Music Partners", # Realistic company name
            "C418 Official Collaborator" # Another realistic example
        ]
        for name in valid_names:
            with self.subTest(name=name):
                is_valid, msg = validate_name(name)
                self.assertTrue(is_valid, f"Valid name {name} should pass")
                self.assertEqual(msg, "", f"Message should be empty for {name}")

        invalid_names = [
            "A",  # Too short (less than 2 characters)
            "Super Long Company Name That Exceeds The Maximum Allowed Length Of Fifty Characters",  # Too long (more than 50 characters)
            ""    # Empty string
        ]
        for name in invalid_names:
            with self.subTest(name=name):
                is_valid, msg = validate_name(name)
                self.assertFalse(is_valid, f"Invalid name {name} should fail")
                self.assertNotEqual(msg, "", f"Error message should be present for {name}")

    def test_validate_description(self):
        """Test description validation: at least 5 letters (a-z, A-Z), total length up to 200 characters."""
        # Valid descriptions: must have at least 5 letters
        valid_descriptions = [
            "abcde",  # Exactly 5 letters
            "A music company",  # More than 5 letters (A, m, u, s, i, c, c, o, m, p, a, n, y)
            "ab12cde!",  # 5 letters (a, b, c, d, e) with numbers and symbols
            "hello123 world456"  # More than 5 letters with numbers
        ]
    
        # Invalid descriptions: less than 5 letters or too long
        invalid_descriptions = [
            "ab12!",  # Only 2 letters (a, b)
            "12345",  # No letters
            "ab cd",  # Only 4 letters (a, b, c, d) with a space
            "x" * 201  # Too long (over 200 characters)
        ]

        # Test valid descriptions
        for desc in valid_descriptions:
            result, error = validate_description(desc)
            self.assertTrue(result, f"Description '{desc}' should be valid, but got error: {error}")

        # Test invalid descriptions
        for desc in invalid_descriptions:
            result, error = validate_description(desc)
            self.assertFalse(result, f"Description '{desc}' should be invalid")

if __name__ == '__main__':
    unittest.main()