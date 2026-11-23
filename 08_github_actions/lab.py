from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "07_testing_pytest"))

from app import Figure, print_info


if __name__ == "__main__":
    print_info(Figure("квадрат", 5))
