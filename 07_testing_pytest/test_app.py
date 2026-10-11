import pytest

from app import Figure, print_info
from conftest import CALLS


# ---------- Основи ----------
@pytest.mark.unit
def test_triangle_type():
    assert Figure("трикутник", 4).type == "трикутник"


@pytest.mark.unit
def test_invalid_length():
    with pytest.raises(AssertionError):
        Figure("квадрат", 0)


def test_invalid_figure():
    with pytest.raises(AssertionError, match="Невідомий тип фігури"):
        Figure("коло", 1)


# ---------- :star: параметризація для всіх дозволених фігур ----------
@pytest.mark.parametrize("figure_type", Figure.FIGURES)
def test_allowed_figure(figure_type):
    assert Figure(figure_type, 1).type == figure_type


@pytest.mark.parametrize(
    "figure_type, length",
    [("квадрат", 1), ("прямокутник", 7), ("трикутник", 100)],
    ids=["square-min", "rectangle-7", "triangle-100"],
)
def test_figure_type_and_length(figure_type, length):
    fig = Figure(figure_type, length)
    assert (fig.type, fig.get_figure_length) == (figure_type, length)


# ---------- :star: fixture з довжиною 10 ----------
def test_square_length(square):
    assert square.get_figure_length == 10


def test_square_type(square):
    assert square.type == "квадрат"


def test_fixture_reused_inside_one_test(square, length):
    # length запитано двічі (тестом і fixture square) — pytest дає те саме значення
    assert square.get_figure_length is length


# ---------- :fire: кожен неправильний тип і кожна неправильна довжина ----------
@pytest.mark.parametrize(
    "bad_type", ["коло", "", "Квадрат", "квадрат ", "ромб", None, 3]
)
def test_each_invalid_type(bad_type):
    with pytest.raises(AssertionError):
        Figure(bad_type, 5)


@pytest.mark.parametrize("bad_length", [0, -1, -100, -0.5])
def test_each_invalid_length(bad_length):
    with pytest.raises(AssertionError, match="Довжина має бути більшою за 0"):
        Figure("квадрат", bad_length)


@pytest.mark.parametrize("bad_length", ["5", None, [5]])
def test_non_numeric_length(bad_length):
    # порівняння str/None/list з 0 у Python 3 кидає TypeError
    with pytest.raises(TypeError):
        Figure("квадрат", bad_length)


# ---------- :star: fixture зі scope="module" у двох тестах ----------
def test_module_fixture_contains_square(allowed_figures):
    assert "квадрат" in allowed_figures


def test_module_fixture_created_once(allowed_figures):
    assert len(allowed_figures) == 3
    assert CALLS["allowed_figures"] == 1


# ---------- вбудовані fixtures: tmp_path + yield, monkeypatch, capsys ----------
@pytest.fixture
def text_file(tmp_path):
    path = tmp_path / "result.txt"
    path.write_text("готово", encoding="utf-8")
    yield path
    path.unlink()  # очищення після тесту


def test_text_file(text_file):
    assert text_file.read_text(encoding="utf-8") == "готово"


def test_monkeypatch_figures(monkeypatch):
    # тимчасово дозволяємо нову фігуру лише в межах цього тесту
    monkeypatch.setattr(Figure, "FIGURES", Figure.FIGURES + ["ромб"])
    assert Figure("ромб", 2).type == "ромб"


def test_monkeypatch_restored():
    assert "ромб" not in Figure.FIGURES


def test_print_info(capsys):
    print_info(Figure("трикутник", 3))
    assert capsys.readouterr().out == "трикутник: довжина 3\n"
