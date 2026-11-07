"""Додаткові тести (:fire:) — доводять покриття до 100 %."""
import pytest

from app import Figure


def test_invalid_type():
    with pytest.raises(AssertionError, match="Невідомий тип фігури"):
        Figure("коло", 1)


def test_figure_attributes():
    fig = Figure("прямокутник", 7)
    assert (fig.type, fig.length) == ("прямокутник", 7)


def test_unknown_type_returns_zero_angles(monkeypatch):
    # Гілка `return 0` недосяжна через валідацію в __init__.
    # Тимчасово розширюємо FIGURES, щоб перевірити захисну гілку.
    monkeypatch.setattr(Figure, "FIGURES", Figure.FIGURES + ["коло"])
    assert Figure("коло", 1).get_angles == 0
