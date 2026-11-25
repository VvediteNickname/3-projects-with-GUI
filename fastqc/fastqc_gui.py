
import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QTextEdit, QMessageBox,
    QTabWidget, QScrollArea,
)

from sequences import FastqReader
from fastqc_plots import build_all_plots


FASTQ_EXTS = (".fastq", ".fq")


class FastQCGui(QMainWindow):

    def __init__(self, initial_file=None):
        super().__init__()
        self.setWindowTitle("FastQC-lite")
        self.setMinimumSize(900, 700)
        self.setAcceptDrops(True)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        top = QHBoxLayout()
        self.open_btn = QPushButton("Выбрать файл…")
        self.open_btn.clicked.connect(self.on_open_clicked)
        top.addWidget(self.open_btn)

        self.path_label = QLabel("Файл не выбран")
        self.path_label.setStyleSheet("color: #555;")
        top.addWidget(self.path_label, stretch=1)
        root.addLayout(top)

        self.stats = QTextEdit()
        self.stats.setReadOnly(True)
        self.stats.setFont(QFont("DejaVu Sans Mono", 11))
        self.stats.setMaximumHeight(120)
        root.addWidget(self.stats)

        self.tabs = QTabWidget()
        root.addWidget(self.tabs, stretch=1)

        if initial_file:
            self.load_file(initial_file)

    def on_open_clicked(self):
        pattern = " ".join(f"*{e}" for e in FASTQ_EXTS)
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите FASTQ файл", "",
            f"FASTQ ({pattern})"
        )
        if path:
            self.load_file(path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                ext = os.path.splitext(url.toLocalFile())[1].lower()
                if ext in FASTQ_EXTS:
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            ext = os.path.splitext(path)[1].lower()
            if ext in FASTQ_EXTS:
                self.load_file(path)
                event.acceptProposedAction()
                return
        event.ignore()

    def load_file(self, path):
        if not path.lower().endswith(FASTQ_EXTS):
            QMessageBox.critical(self, "Ошибка", "Поддерживаются только FASTQ (*.fastq, *.fq)")
            return

        reader = FastqReader(path)

        self.path_label.setText(path)
        self.stats.clear()
        self.tabs.clear()

        count = reader.get_sequences_count()
        avg = reader.get_average_length()

        self.stats.append(f"Файл: {path}")
        self.stats.append(f"Число последовательностей: {count}")
        self.stats.append(f"Средняя длина: {avg:.2f}")

        for title, result in build_all_plots(reader):
            if os.path.exists(result):
                tab = self._make_plot_tab(result)
            else:
                tab = QLabel(f"{title}\n{result}")
                tab.setAlignment(Qt.AlignCenter)
            self.tabs.addTab(tab, title)

    def _make_plot_tab(self, image_path):
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