import unittest

from app import Figure


class TestFigure(unittest.TestCase):
    """Тести класу Figure: тип, довжина, кути та некоректні дані."""

    @classmethod
    def setUpClass(cls) -> None:
        # Виконується один раз перед усіма тестами класу
        cls.valid_types = list(Figure.FIGURES)

    def setUp(self) -> None:
        # Виконується перед КОЖНИМ тестом — кожен тест отримує свіжий об'єкт
        self.obj = Figure("квадрат", 5)

    def tearDown(self) -> None:
        # Виконується після кожного тесту
        del self.obj

    # --- базові тести з прикладу ---
    def test_figure_type(self):
        self.assertEqual("квадрат", self.obj.get_figure_type)

    def test_figure_length(self):
        self.assertEqual(5, self.obj.get_figure_length)

    def test_invalid_figure(self):
        with self.assertRaises(ValueError):
            Figure("коло", 1)

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            Figure("квадрат", 0)

    # --- :star: get_angles ---
    def test_angles_square(self):
        self.assertEqual(4, Figure("квадрат", 3).get_angles)

    def test_angles_rectangle(self):
        self.assertEqual(4, Figure("прямокутник", 3).get_angles)

    def test_angles_triangle(self):
        self.assertEqual(3, Figure("трикутник", 3).get_angles)

    # --- :fire: граничні та некоректні дані ---
    def test_zero_length(self):
        with self.assertRaises(ValueError):
            Figure("трикутник", 0)

    def test_negative_length(self):
        with self.assertRaises(ValueError):
            Figure("прямокутник", -5)

    def test_unknown_figure_type(self):
        with self.assertRaisesRegex(ValueError, "Невідомий тип фігури"):
            Figure("шестикутник", 2)

    def test_length_wrong_type(self):
        with self.assertRaises(TypeError):
            Figure("квадрат", "5")

    def test_minimal_valid_length(self):
        # граничне значення: 1 — найменша допустима довжина
        self.assertEqual(1, Figure("квадрат", 1).get_figure_length)

    # --- :star: subTest для всіх типів фігур ---
    def test_all_figure_types(self):
        expected_angles = {"квадрат": 4, "прямокутник": 4, "трикутник": 3}
        for figure_type in self.valid_types:
            for length in [1, 5, 10]:
                with self.subTest(figure_type=figure_type, length=length):
                    fig = Figure(figure_type, length)
                    self.assertEqual(figure_type, fig.get_figure_type)
                    self.assertEqual(length, fig.get_figure_length)
                    self.assertEqual(expected_angles[figure_type], fig.get_angles)


if __name__ == "__main__":
    unittest.main(verbosity=2)
