class Figure:
    FIGURES = ["квадрат", "прямокутник", "трикутник"]
    ANGLES = {"квадрат": 4, "прямокутник": 4, "трикутник": 3}

    def __init__(self, figure_type: str, length: int) -> None:
        # assert вимикається при запуску `python -O`, тому для перевірки
        # аргументів використовуємо явні винятки.
        if isinstance(length, bool) or not isinstance(length, (int, float)):
            raise TypeError("Довжина має бути числом!")
        if length <= 0:
            raise ValueError("Довжина має бути більшою за 0!")
        if figure_type not in self.FIGURES:
            raise ValueError("Невідомий тип фігури")
        self.type = figure_type
        self.length = length

    @property
    def get_figure_type(self) -> str:
        return self.type

    @property
    def get_figure_length(self) -> int:
        return self.length

    @property
    def get_angles(self) -> int:
        return self.ANGLES[self.type]


if __name__ == "__main__":
    # ручна перевірка властивостей
    for t, l in [("квадрат", 5), ("прямокутник", 3), ("трикутник", 7)]:
        f = Figure(t, l)
        print(f"{f.get_figure_type:<12} довжина={f.get_figure_length:<3} кутів={f.get_angles}")
