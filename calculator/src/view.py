from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QLineEdit, QLabel, QPushButton,
)


class CalculatorView(QMainWindow):
    """View на PySide6. Публичный API совместим с контроллером."""

    # ---------- палитра ----------
    BG         = "#84b66a"
    BTN_BG     = "#5B7820"
    BTN_HOVER  = "#216957"
    BTN_PRESS  = "#889828"
    BTN_FG     = "#ffffff"
    ENTRY_BG   = "#ffffff"
    ENTRY_FG   = "#000000"
    ERROR_FG   = "#fb2b51"

    BTN_SIZE = 70

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculator")
        self.setMinimumSize(420, 620)

        # Колбэки, которые установит контроллер
        self.callbacks = {}

        # Центральный виджет
        central = QWidget(self)
        central.setStyleSheet(f"background-color: {self.BG};")
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(10)

        # Поле отображения
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setFont(QFont("Noto Sans", 24))
        self.display.setText("0")
        self.display.setFocusPolicy(Qt.StrongFocus)
        self.display.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.ENTRY_BG};
                color: {self.ENTRY_FG};
                border: 2px solid {self.BTN_BG};
                border-radius: 12px;
                padding: 10px 14px;
            }}
        """)
        root.addWidget(self.display)

        # Метка ошибок
        self.status_label = QLabel("")
        self.status_label.setStyleSheet(
            f"color: {self.ERROR_FG}; font-size: 12px; background: transparent;"
        )
        self.status_label.setAlignment(Qt.AlignLeft)
        root.addWidget(self.status_label)

        # Сетка кнопок
        grid = QGridLayout()
        grid.setSpacing(10)
        root.addLayout(grid, stretch=1)

        layout = [
            ("C",  0, 0, "clear", None),
            ("⌫", 0, 1, "backspace", None),
            ("√",  0, 2, "sqrt", None),
            ("/",  0, 3, "operator", "/"),

            ("7", 1, 0, "digit", "7"),
            ("8", 1, 1, "digit", "8"),
            ("9", 1, 2, "digit", "9"),
            ("*", 1, 3, "operator", "*"),

            ("4", 2, 0, "digit", "4"),
            ("5", 2, 1, "digit", "5"),
            ("6", 2, 2, "digit", "6"),
            ("-", 2, 3, "operator", "-"),

            ("1", 3, 0, "digit", "1"),
            ("2", 3, 1, "digit", "2"),
            ("3", 3, 2, "digit", "3"),
            ("+", 3, 3, "operator", "+"),

            ("0", 4, 0, "digit", "0"),
            (".", 4, 1, "digit", "."),
            ("=", 4, 2, "equals", None),
        ]

        for text, row, col, kind, value in layout:
            if kind == "equals":
                command = self._emit_equals
                colspan = 2
                bg, hover, press = "#556B2F", "#6B8E23", "#7BA428"
            else:
                command = lambda k=kind, v=value: self._emit(k, v)
                colspan = 1
                bg, hover, press = self.BTN_BG, self.BTN_HOVER, self.BTN_PRESS

            btn = QPushButton(text)
            btn.setFixedSize(self.BTN_SIZE, self.BTN_SIZE)
            btn.setFont(QFont("Arial", 16, QFont.Bold))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFocusPolicy(Qt.NoFocus)          # ← кнопки не забирают фокус
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg};
                    color: {self.BTN_FG};
                    border: none;
                    border-radius: {self.BTN_SIZE // 2}px;
                    font-size: 16px;
                    font-weight: bold;
                }}
                QPushButton:hover   {{ background-color: {hover}; }}
                QPushButton:pressed {{ background-color: {press}; }}
            """)
            btn.clicked.connect(lambda _=False, c=command: c())
            grid.addWidget(btn, row, col, 1, colspan)

        for c in range(4):
            grid.setColumnStretch(c, 1)
        for r in range(5):
            grid.setRowStretch(r, 1)

        self.display.setFocus()

    # ---------- клавиатура ----------

    def keyPressEvent(self, event):
        key = event.key()
        ch = event.text()

        if ch.isdigit() or ch == ".":
            self._emit("digit", ch)
        elif ch in "+-*/":
            self._emit("operator", ch)
        elif key in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Equal):
            self._emit("equals", None)
        elif key == Qt.Key_Backspace:
            self._emit("backspace", None)
        elif key == Qt.Key_Escape:
            self._emit("clear", None)
        else:
            super().keyPressEvent(event)

    # ---------- проброс событий ----------

    def _emit(self, kind, value):
        handler = self.callbacks.get(kind)
        if handler is None:
            return
        if value is None:
            handler()
        else:
            handler(value)

    def _emit_equals(self):
        self._emit("equals", None)

    # ---------- публичный API ----------

    def set_display(self, value):
        self.display.setText(str(value))

    def get_display(self):
        return self.display.text()

    def show_error(self, message):
        self.status_label.setText(message)

    def clear_error(self):
        self.status_label.setText("")

    def set_callbacks(self, callbacks):
        self.callbacks = callbacks