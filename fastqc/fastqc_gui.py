import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QTextEdit, QMessageBox,
    QTabWidget, QScrollArea,
)

from sequences import FastaReader, FastqReader
from fastqc_plots import build_all_plots

FASTA_EXTS = (".fasta", ".fa", ".fna")
FASTQ_EXTS = (".fastq", ".fq")
ALL_EXTS = FASTA_EXTS + FASTQ_EXTS


# Стиль: применяется к окну и наследуется всеми диалогами (parent=self)
LILAC_STYLE = """
QWidget { font-size: 13px; color: #3f3763; }
#root { background-color: #f3f0fa; }
QLabel { color: #4a4169; background: transparent; }
#pathLabel { color: #8a81a8; }

QPushButton {
    background-color: #ffffff; color: #5a4f82;
    border: 1px solid #ddd3f5; border-radius: 10px;
    padding: 9px 18px; font-weight: 600;
}
QPushButton:hover { background-color: #f1ecfb; }
QPushButton:pressed { background-color: #e6def8; }

#openBtn { background-color: #8b5cf6; color: white; border: none; }
#openBtn:hover { background-color: #7c3aed; }
#openBtn:pressed { background-color: #6d28d9; }

QTextEdit {
    background-color: #ffffff;
    border: 1px solid #ddd3f5; border-radius: 10px;
    padding: 8px;
    selection-background-color: #8b5cf6; selection-color: #ffffff;
}

QTabWidget::pane {
    border: 1px solid #ddd3f5; border-radius: 12px;
    background-color: #ffffff;
}
QTabBar::tab {
    background-color: #e9e3f7; color: #6f6595;
    padding: 8px 18px; margin: 4px 4px 0 0;
    border-top-left-radius: 10px; border-top-right-radius: 10px;
    font-weight: 600;
}
QTabBar::tab:selected {
    background-color: #ffffff; color: #6d28d9;
    border: 1px solid #ddd3f5; border-bottom: none;
}
QTabBar::tab:hover:!selected { background-color: #dfd7f2; }

QScrollArea { border: none; background: transparent; }

QScrollBar:vertical { background: #efeaf9; width: 10px; margin: 2px; border-radius: 5px; }
QScrollBar::handle:vertical { background: #b8a8e8; border-radius: 5px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: #a28fe0; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: #efeaf9; height: 10px; margin: 2px; border-radius: 5px; }
QScrollBar::handle:horizontal { background: #b8a8e8; border-radius: 5px; min-width: 30px; }
QScrollBar::handle:horizontal:hover { background: #a28fe0; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

QDialog { background-color: #f7f4fc; }
"""


def _pick_reader(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in FASTA_EXTS:
        return FastaReader(path)
    if ext in FASTQ_EXTS:
        return FastqReader(path)
    raise ValueError(f"Неизвестный формат файла: {ext}")


class FastQCGui(QMainWindow):

    def __init__(self, initial_file=None):
        super().__init__()
        self.setWindowTitle("FastQC-lite")
        self.setMinimumSize(900, 700)
        self.setAcceptDrops(True)

        # Центральный виджет + сиреневый стиль
        central = QWidget()
        central.setObjectName("root")
        central.setAttribute(Qt.WA_StyledBackground, True)
        self.setCentralWidget(central)
        self.setStyleSheet(LILAC_STYLE)

        root = QVBoxLayout(central)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        # --- верхняя панель ---
        top = QHBoxLayout()
        top.setSpacing(10)

        self.open_btn = QPushButton("Выбрать файл…")
        self.open_btn.setObjectName("openBtn")
        self.open_btn.clicked.connect(self.on_open_clicked)
        top.addWidget(self.open_btn)

        self.path_label = QLabel("Файл не выбран")
        self.path_label.setObjectName("pathLabel")
        top.addWidget(self.path_label, stretch=1)

        root.addLayout(top)

        # --- краткая статистика ---
        self.stats = QTextEdit()
        self.stats.setReadOnly(True)
        self.stats.setFont(QFont("DejaVu Sans Mono", 11))
        self.stats.setMaximumHeight(120)
        root.addWidget(self.stats)

        # --- вкладки с графиками ---
        self.tabs = QTabWidget()
        root.addWidget(self.tabs, stretch=1)

        if initial_file:
            self.load_file(initial_file)

    def on_open_clicked(self):
        pattern = " ".join(f"*{e}" for e in ALL_EXTS)
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите FASTA/FASTQ файл", "",
            f"Биологические файлы ({pattern});;Все файлы (*)"
        )
        if path:
            self.load_file(path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                ext = os.path.splitext(url.toLocalFile())[1].lower()
                if ext in ALL_EXTS:
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            ext = os.path.splitext(path)[1].lower()
            if ext in ALL_EXTS:
                self.load_file(path)
                event.acceptProposedAction()
                return
        event.ignore()

    def load_file(self, path):
        try:
            reader = _pick_reader(path)
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            return

        self.path_label.setText(path)
        self.stats.clear()
        self.tabs.clear()

        count = reader.get_sequences_count()
        avg = reader.get_average_length()

        self.stats.append(f"Файл: {path}")
        self.stats.append(f"Число последовательностей: {count}")
        self.stats.append(f"Средняя длина: {avg:.2f}")

        # строим все графики и раскладываем по вкладкам
        for title, result in build_all_plots(reader):
            if os.path.exists(result):
                tab = self._make_plot_tab(result)
            else:
                tab = QLabel(f"{title}\n{result}")
                tab.setAlignment(Qt.AlignCenter)
            self.tabs.addTab(tab, title)

    def _make_plot_tab(self, image_path):
        """QLabel с картинкой внутри QScrollArea, чтобы большие графики можно было скроллить."""
        label = QLabel()
        label.setAlignment(Qt.AlignCenter)
        pix = QPixmap(image_path)
        if not pix.isNull():
            label.setPixmap(pix.scaled(
                860, 560, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        else:
            label.setText("Не удалось загрузить график")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(label)
        return scroll


def run_gui(initial_file=None):
    app = QApplication.instance() or QApplication(sys.argv)
    win = FastQCGui(initial_file=initial_file)
    win.show()
    sys.exit(app.exec())