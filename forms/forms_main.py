
import sys

from PySide6.QtWidgets import QApplication

from forms_model import FormsModel
from forms_view import FormsView
from forms_controller import FormsController


def main():
    app = QApplication(sys.argv)

    model = FormsModel()
    view = FormsView()
    controller = FormsController(model, view)

    view.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

