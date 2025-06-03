import unittest
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to sys.path to import actual_new_logic
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from actual_new_logic import is_valid_author, is_valid_description, is_valid_date, is_valid_date_range

class TestFormValidation(unittest.TestCase):
    def test_author_validation(self):
        """Test is_valid_author for valid, invalid, and edge cases."""
        valid_authors = [
            "C418 Song",
            "C418-Track_01",
            "Ab123",
            "AuthorName123"
        ]
        for author in valid_authors:
            with self.subTest(author=author):
                self.assertTrue(is_valid_author(author), f"Author '{author}' should be valid")

        invalid_authors = [
            "Ab",  # Too short
            "A" * 51,  # Too long
            "123",  # Only digits
            "C418####",  # Repeated special chars
            "C418  Song",  # Multiple spaces
            "test_nonlatin",  # Placeholder for non-Latin
            "C418_smile",  # Placeholder for emoji
            "shit song"  # Profanity
        ]
        for author in invalid_authors:
            with self.subTest(author=author):
                self.assertFalse(is_valid_author(author), f"Author '{author}' should be invalid")

        edge_cases = [
            "",  # Empty string
            "-C418",  # Starts with hyphen
            "C418-",  # Ends with hyphen
            "C418<script>",  # HTML-like
            "C418@Song"  # Invalid special char
        ]
        for author in edge_cases:
            with self.subTest(author=author):
                self.assertFalse(is_valid_author(author), f"Edge case author '{author}' should be invalid")

    def test_description_validation(self):
        """Test is_valid_description for valid, invalid, and edge cases."""
        valid_descriptions = [
            "This is a new C418 song.",
            "A" * 10 + " valid song",
            "This song has three words!",
            "Description with punctuation: hello, world!"
        ]
        for desc in valid_descriptions:
            with self.subTest(description=desc):
                self.assertTrue(is_valid_description(desc), f"Description '{desc[:50]}...' should be valid")

        invalid_descriptions = [
            "Short",  # Too short
            "A" * 1001,  # Too long
            "One two",  # Less than 3 words
            "<script>alert(1)</script>",  # HTML tags
            "This is smile song",  # Placeholder for emoji
            "This   is spaced",  # Multiple spaces
            "test_nonlatin desc",  # Placeholder for non-Latin
            "fuck this song"  # Profanity
        ]
        for desc in invalid_descriptions:
            with self.subTest(description=desc):
                self.assertFalse(is_valid_description(desc), f"Description '{desc[:50]}..' should be invalid")

        edge_cases = [
            "",  # Empty string
            "A B C",  # Three single-letter words
            "This is a<script>",  # Partial HTML
            "This!!!is...punctuated",  # Heavy punctuation
            "\n\t\r"  # Control characters
        ]
        for desc in edge_cases:
            with self.subTest(description=desc):
                self.assertFalse(is_valid_description(desc), f"Edge case description '{desc[:50]}...' should be invalid")

    def test_date_validation(self):
        """Test is_valid_date and is_valid_date_range for valid, invalid, and edge cases."""
        valid_dates = [
            (datetime.now() + timedelta(days=1)).strftime('%d.%m.%Y'),
            "03.06.2025",
            "29.02.2028",
            (datetime.now() + timedelta(days=365 * 10)).strftime('%d.%m.%Y')
        ]
        for date in valid_dates:
            with self.subTest(date=date, test="is_valid_date"):
                self.assertTrue(is_valid_date(date), f"Date '{date}' should have valid format")
            with self.subTest(date=date, test="is_valid_date_range"):
                is_valid, error_msg = is_valid_date_range(date)
                self.assertTrue(is_valid, f"Date '{date}' should be in valid range, got error: '{error_msg}'")
                self.assertEqual(error_msg, "", f"Date '{date}' should have empty error message")

        invalid_dates = [
            "32.06.2025",  # Invalid day
            "31.13.2025",  # Invalid month
            "29.02.2027",  # Non-leap year
            "3.06.2025",  # Missing leading zero
            "03/06/2025",  # Wrong separator
            "abc",  # Non-date
            ""  # Empty
        ]
        for date in invalid_dates:
            with self.subTest(date=date, test="is_valid_date"):
                self.assertFalse(is_valid_date(date), f"Date '{date}' should be invalid format")

        invalid_range_dates = [
            (datetime.now() - timedelta(days=1)).strftime('%d.%m.%Y'),  # Past date
            (datetime.now() + timedelta(days=365 * 11)).strftime('%d.%m.%Y'),  # Beyond 10 years
            "abc"  # Invalid format
        ]
        for date in invalid_range_dates:
            with self.subTest(date=date, test="is_valid_date_range"):
                is_valid, error_msg = is_valid_date_range(date)
                self.assertFalse(is_valid, f"Date '{date}' should be invalid range")
                self.assertNotEqual(error_msg, "", f"Date '{date}' should have an error message")

if __name__ == '__main__':
    unittest.main(verbosity=2)