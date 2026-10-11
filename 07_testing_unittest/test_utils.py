import unittest
from unittest.mock import patch

from utils import ask_age, count_symbols, count_vowels, divide, validate_age


class TestValidateAge(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(19, validate_age("19"))
        self.assertEqual(42, validate_age("  42 "))

    def test_boundaries(self):
        for value, expected in [("1", 1), ("120", 120)]:
            with self.subTest(value=value):
                self.assertEqual(expected, validate_age(value))

    def test_invalid_input(self):
        for value in ["", "   ", "abc", "4.5", "0", "-3", "121"]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_age(value)


class TestCountSymbols(unittest.TestCase):
    def test_count_symbols(self):
        self.assertEqual(3, count_symbols("abc"))
        self.assertEqual(0, count_symbols(""))
        self.assertEqual(1, count_symbols(" "))


class TestDivide(unittest.TestCase):
    def test_divide(self):
        self.assertEqual(2, divide(10, 5))
        self.assertAlmostEqual(0.333, divide(1, 3), places=3)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(1, 0)


class TestCountVowels(unittest.TestCase):
    def test_latin(self):
        self.assertEqual(5, count_vowels("Education"))

    def test_only_consonants(self):
        self.assertEqual(0, count_vowels("rhythm"))

    def test_mixed_case(self):
        self.assertEqual(4, count_vowels("AeIo"))

    # :fire: порожній рядок, цифри, українські літери
    def test_empty_string(self):
        self.assertEqual(0, count_vowels(""))

    def test_digits(self):
        self.assertEqual(0, count_vowels("1234567890"))
        self.assertEqual(2, count_vowels("a1b2e3"))

    def test_ukrainian(self):
        self.assertEqual(4, count_vowels("Україна"))  # У, а, ї, а
        self.assertEqual(6, count_vowels("Їжак їсть яблуко"))
        self.assertEqual(4, count_vowels("ЄИІЮ"))

    def test_not_a_string(self):
        with self.assertRaises(TypeError):
            count_vowels(None)


class TestAskAge(unittest.TestCase):
    @patch("builtins.input", return_value="19")
    def test_ask_age_valid(self, mock_input):
        self.assertEqual(19, ask_age())
        mock_input.assert_called_once_with("Введіть ваш вік: ")

    @patch("builtins.input", side_effect=["abc"])
    def test_ask_age_invalid(self, mock_input):
        with self.assertRaises(ValueError):
            ask_age()
        mock_input.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)
