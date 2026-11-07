"""Лише демонстрація запуску; логіка Figure тестується окремо."""
from app import Figure


def main():
    return Figure("трикутник", 1).get_angles


if __name__ == "__main__":  # pragma: no cover
    print(main())
