"""Спільні fixtures — pytest знаходить їх автоматично, імпорт не потрібен."""
import pytest

from app import Figure

# лічильник викликів, щоб довести, що module-fixture створюється один раз
CALLS = {"allowed_figures": 0}


@pytest.fixture(scope="module")
def allowed_figures():
    CALLS["allowed_figures"] += 1
    return tuple(Figure.FIGURES)


@pytest.fixture
def length():
    return 10


@pytest.fixture
def square(length):
    # fixture, що залежить від іншої fixture (length)
    return Figure("квадрат", length)
