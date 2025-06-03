import unittest
from datetime import datetime, timedelta
from actual_new_logic import is_valid_author, is_valid_description, is_valid_date, is_valid_date_range

class TestFormValidation(unittest.TestCase):
    """Unit tests for form field validation in actual_new_logic.py."""

    def test_is_valid_author_valid_cases(self):
        """Test valid author inputs."""
        valid_authors = [
            "C418 Song",  # Normal case with space
            "C418-Track_01",  # With hyphen and underscore
            "Ab123",  # Mixed letters and digits, minimum length
            "A" * 50  # Maximum length
        ]
        for author in valid_authors:
            with self.subTest(author=author):
                self.assertTrue(
                    is_valid_author(author),
                    f"Author '{author}' should be valid"
                )

    def test_is_valid_author_invalid_cases(self):
        """Test invalid author inputs."""
        invalid_authors = [
            "Ab",  # Too short
            "A" * 51,  # Too long
            "123",  # Only digits
            "C418####",  # Repeated special chars
            "C418  Song",  # Multiple spaces
            "Песня",  # Cyrillic
            "C418??",  # Emoji
            "shit song"  # Profanity
        ]
        for author in invalid_authors:
            with self.subTest(author=author):
                self.assertFalse(
                    is_valid_author(author),
                    f"Author '{author}' should be invalid"
                )

    def test_is_valid_author_edge_cases(self):
        """Test edge cases for author validation."""
        edge_cases = [
            "-C418",  # Starts with hyphen
            "C418-",  # Ends with hyphen
            "",  # Empty string
            "C418<script>",  # HTML-like
            "C418@Song"  # Invalid special char
        ]
        for author in edge_cases:
            with self.subTest(author=author):
                self.assertFalse(
                    is_valid_author(author),
                    f"Edge case author '{author}' should be invalid"
                )

    def test_is_valid_description_valid_cases(self):
        """Test valid description inputs."""
        valid_descriptions = [
            "This is a new C418 song.",  # Simple valid case
            "A" * 10,  # Minimum length
            "A" * 1000,  # Maximum length
            "This song has three words!"  # Exactly 3 words with punctuation
        ]
        for desc in valid_descriptions:
            with self.subTest(description=desc):
                self.assertTrue(
                    is_valid_description(desc),
                    f"Description '{desc[:50]}...' should be valid"
                )

    def test_is_valid_description_invalid_cases(self):
        """Test invalid description inputs."""
        invalid_descriptions = [
            "Short",  # Too short
            "A" * 1001,  # Too long
            "One two",  # Less than 3 words
            "<script>alert(1)</script>",  # HTML tags
            "This is ?? song",  # Emoji
            "This   is spaced",  # Multiple spaces
            "Песня C418",  # Cyrillic
            "Fuck this song"  # Profanity
        ]
        for desc in invalid_descriptions:
            with self.subTest(description=desc):
                self.assertFalse(
                    is_valid_description(desc),
                    f"Description '{desc[:50]}...' should be invalid"
                )

    def test_is_valid_description_edge_cases(self):
        """Test edge cases for description validation."""
        edge_cases = [
            "",  # Empty string
            "A B C",  # Three single-letter words
            "This is a<script>",  # Partial HTML
            "This!!!is...punctuated",  # Heavy punctuation
            "\n\t\r"  # Control characters
        ]
        for desc in edge_cases:
            with self.subTest(description=desc):
                self.assertFalse(
                    is_valid_description(desc),
                    f"Edge case description '{desc[:50]}...' should be invalid"
                )

    def test_is_valid_date_format(self):
        """Test date format validation."""
        valid_dates = [
            "03.06.2025",  # Current date
            "31.12.2030",  # Valid future date
            "29.02.2028"  # Valid leap year
        ]
        invalid_dates = [
            "32.06.2025",  # Invalid day
            "31.13.2025",  # Invalid month
            "29.02.2027",  # Non-leap year
            "3.06.2025",  # Missing leading zero
            "03/06/2025",  # Wrong separator
            "abc",  # Non-date
            ""  # Empty
        ]
        for date in valid_dates:
            with self.subTest(date=date):
                self.assertTrue(
                    is_valid_date(date),
                    f"Date '{date}' should be valid"
                )
        for date in invalid_dates:
            with self.subTest(date=date):
                self.assertFalse(
                    is_valid_date(date),
                    f"Date '{date}' should be invalid"
                )

    def test_is_valid_date_range_valid(self):
        """Test valid date range inputs."""
        valid_ranges = [
            "03.06.2025",  # Today
            "04.06.2025",  # Tomorrow
            "03.06.2035"  # Exactly 10 years
        ]
        for date in valid_ranges:
            with self.subTest(date=date):
                is_valid, error_msg = is_valid_date_range(date)
                self.assertTrue(
                    is_valid,
                    f"Date '{date}' should be valid with no error, got '{error_msg}'"
                )
                self.assertEqual(
                    error_msg,
                    "",
                    f"Date '{date}' should have empty error message"
                )

    def test_is_valid_date_range_invalid(self):
        """Test invalid date range inputs."""
        invalid_ranges = [
            ("02.06.2025", "Date cannot be before today."),
            ("04.06.2035", "Date cannot be more than 10 years from today."),
            ("invalid", "Invalid date.")
        ]
        for date, expected_error in invalid_ranges:
            with self.subTest(date=date):
                is_valid, error_msg = is_valid_date_range(date)
                self.assertFalse(
                    is_valid,
                    f"Date '{date}' should be invalid"
                )
                self.assertEqual(
                    error_msg,
                    expected_error,
                    f"Date '{date}' should return error '{expected_error}', got '{error_msg}'"
                )

if __name__ == '__main__':
    unittest.main()