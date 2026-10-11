"""Функції для частин «Перевірка даних» та «Тестування функцій»."""

VOWELS = set("aeiouAEIOU" + "аеєиіїоуюяАЕЄИІЇОУЮЯ")


def validate_age(value: str) -> int:
    """:star: Власна перевірка введеного числа: вік у межах 1..120."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Значення не може бути порожнім")
    try:
        age = int(value.strip())
    except ValueError:
        raise ValueError(f"'{value}' не є цілим числом") from None
    if not 1 <= age <= 120:
        raise ValueError(f"Вік має бути в межах 1..120, отримано {age}")
    return age


def count_symbols(text: str) -> int:
    return len(text)


def divide(a: float, b: float) -> float:
    return a / b


def count_vowels(text: str) -> int:
    """:star: Кількість голосних (латиниця + українська абетка)."""
    if not isinstance(text, str):
        raise TypeError("Очікується рядок")
    return sum(1 for ch in text if ch in VOWELS)


def ask_age() -> int:
    """:star: Функція з input() — тестується через unittest.mock.patch."""
    raw = input("Введіть ваш вік: ")
    return validate_age(raw)


if __name__ == "__main__":
    for raw in ["19", "  42 ", "abc", "", "-3", "150"]:
        try:
            print(f"{raw!r:>8} -> OK: {validate_age(raw)}")
        except ValueError as e:
            print(f"{raw!r:>8} -> ValueError: {e}")

    # assert — перевірка тверджень (зникає при запуску python -O)
    number = -1
    try:
        assert number > 0, "Число має бути більшим за нуль!"
    except AssertionError as e:
        print(f"assert: AssertionError: {e}")
