import sys
import traceback

from PySide6.QtWidgets import QApplication

from view import CalculatorView
from controller import CalculatorController


def excepthook(exc_type, exc_value, exc_tb):
    traceback.print_exception(exc_type, exc_value, exc_tb)


def main():
    sys.excepthook = excepthook          # видеть исключения в слотах

    app = QApplication(sys.argv)
    view = CalculatorView()
    controller = CalculatorController(view)   # ДО show()
    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()