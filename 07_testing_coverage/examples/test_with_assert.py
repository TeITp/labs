from app import Figure


def test_triangle():
    assert Figure("трикутник", 1).get_angles == 3
