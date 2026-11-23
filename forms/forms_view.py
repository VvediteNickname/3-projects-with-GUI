
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit, QComboBox,
    QSpinBox, QDoubleSpinBox, QCheckBox,
    QMessageBox, QDialogButtonBox, QLabel,
    QHeaderView, QAbstractItemView
)
from PySide6.QtCore import Qt

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg


# ============================================================
# СТИЛЬ ПРИЛОЖЕНИЯ
# ============================================================

COLD_STYLE = """
QWidget {
    font-family: "Arial";
    font-size: 13px;
    color: #0f172a;
}

QMainWindow {
    background-color: #eef2f6;
}

QDialog {
    background-color: #f4f7fb;
}

QWidget#root {
    background-color: #eef2f6;
}

QLabel {
    color: #334155;
    background: transparent;
}

QPushButton {
    background-color: #ffffff;
    color: #334155;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #f1f5f9;
}

QPushButton:pressed {
    background-color: #e2e8f0;
}

QPushButton:disabled {
    background-color: #e2e8f0;
    color: #94a3b8;
}

/* Кнопка добавления */

QPushButton#addButton {
    background-color: #2563eb;
    color: white;
    border: none;
}

QPushButton#addButton:hover {
    background-color: #1d4ed8;
}

QPushButton#addButton:pressed {
    background-color: #1e40af;
}

/* Кнопка редактирования */

QPushButton#editButton {
    background-color: #0891b2;
    color: white;
    border: none;
}

QPushButton#editButton:hover {
    background-color: #0e7490;
}

QPushButton#editButton:pressed {
    background-color: #155e75;
}

/* Кнопка удаления */

QPushButton#deleteButton {
    background-color: #e11d48;
    color: white;
    border: none;
}

QPushButton#deleteButton:hover {
    background-color: #be123c;
}

QPushButton#deleteButton:pressed {
    background-color: #9f1239;
}

/* Кнопка статистики */

QPushButton#statsButton {
    background-color: #475569;
    color: white;
    border: none;
}

QPushButton#statsButton:hover {
    background-color: #334155;
}

QPushButton#statsButton:pressed {
    background-color: #1e293b;
}

/* Поля ввода */

QLineEdit,
QSpinBox,
QDoubleSpinBox,
QComboBox {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 7px 10px;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
}

QLineEdit:focus,
QSpinBox:focus,
QDoubleSpinBox:focus,
QComboBox:focus {
    border: 1px solid #2563eb;
}

QLineEdit:disabled {
    background-color: #e2e8f0;
    color: #94a3b8;
}

/* Выпадающий список */

QComboBox::drop-down {
    border: none;
    width: 22px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    selection-background-color: #dbeafe;
    selection-color: #1e3a8a;
}

/* Флажок */

QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
}

QCheckBox::indicator:checked {
    background-color: #2563eb;
    border-color: #2563eb;
}

/* Таблица */

QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    gridline-color: transparent;
    selection-background-color: #dbeafe;
    selection-color: #1e3a8a;
}

QTableWidget::item {
    padding: 8px;
    border: none;
}

QTableWidget::item:selected {
    background-color: #dbeafe;
    color: #1e3a8a;
}

QHeaderView::section {
    background-color: #e2e8f0;
    color: #334155;
    padding: 10px 6px;
    border: none;
    font-weight: 600;
}

/* Полоса прокрутки */

QScrollBar:vertical {
    background-color: #eef2f6;
    width: 10px;
    margin: 2px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #94a3b8;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #64748b;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: #eef2f6;
    height: 10px;
    margin: 2px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background-color: #94a3b8;
    border-radius: 5px;
    min-width: 30px;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0;
}

QDialogButtonBox QPushButton {
    min-width: 90px;
}
"""


# ============================================================
# ДИАЛОГ ДОБАВЛЕНИЯ И РЕДАКТИРОВАНИЯ ПАЦИЕНТА
# ============================================================

class PatientDialog(QDialog):

    def __init__(self, patient=None, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Информация о пациенте")
        self.setMinimumWidth(380)

        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # Фамилия
        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("Введите фамилию")
        layout.addRow("Фамилия:", self.surname_input)

        # Имя
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите имя")
        layout.addRow("Имя:", self.name_input)

        # Отчество
        self.patronymic_input = QLineEdit()
        self.patronymic_input.setPlaceholderText("Введите отчество")

        self.no_patronymic = QCheckBox("Отчества нет")
        self.no_patronymic.toggled.connect(
            self.patronymic_input.setDisabled
        )

        layout.addRow("Отчество:", self.patronymic_input)
        layout.addRow("", self.no_patronymic)

        # Пол
        self.sex_input = QComboBox()
        self.sex_input.addItems([
            "Женский",
            "Мужской",
            "Не определён"
        ])
        layout.addRow("Пол:", self.sex_input)

        # Возраст
        self.age_input = QSpinBox()
        self.age_input.setRange(0, 120)
        self.age_input.setSuffix(" лет")
        layout.addRow("Возраст:", self.age_input)

        # Рост
        self.height_input = QDoubleSpinBox()
        self.height_input.setRange(30, 250)
        self.height_input.setDecimals(1)
        self.height_input.setSuffix(" см")
        layout.addRow("Рост:", self.height_input)

        # Вес
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(1, 500)
        self.weight_input.setDecimals(1)
        self.weight_input.setSuffix(" кг")
        layout.addRow("Вес:", self.weight_input)

        # Кнопки подтверждения
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)

        # Заполняем форму, если редактируем существующего пациента
        if patient is not None:
            self.surname_input.setText(patient["surname"])
            self.name_input.setText(patient["name"])
            self.patronymic_input.setText(patient["patronymic"])

            if not patient["patronymic"]:
                self.no_patronymic.setChecked(True)

            self.sex_input.setCurrentText(patient["sex"])
            self.age_input.setValue(patient["age"])
            self.height_input.setValue(patient["height_cm"])
            self.weight_input.setValue(patient["weight_kg"])

    def get_data(self):
        """Возвращает введённые данные в виде словаря."""

        return {
            "surname": self.surname_input.text().strip(),
            "name": self.name_input.text().strip(),

            "patronymic": (
                ""
                if self.no_patronymic.isChecked()
                else self.patronymic_input.text().strip()
            ),

            "sex": self.sex_input.currentText(),
            "age": self.age_input.value(),
            "height_cm": self.height_input.value(),
            "weight_kg": self.weight_input.value()
        }


# ============================================================
# ОКНО СО СТАТИСТИКОЙ
# ============================================================

class StatisticsDialog(QDialog):

    def __init__(self, patients, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Статистика пациентов")
        self.resize(1000, 750)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        figure = Figure(figsize=(10, 7))
        self.canvas = FigureCanvasQTAgg(figure)

        layout.addWidget(self.canvas)

        self.draw_charts(figure, patients)

    def draw_charts(self, figure, patients):

        # Данные для графиков
        sexes = ["Женский", "Мужской", "Не определён"]

        sex_counts = [
            sum(p["sex"] == sex for p in patients)
            for sex in sexes
        ]

        ages = [p["age"] for p in patients]

        bmi_by_sex = {
            sex: [
                p["bmi"] for p in patients
                if p["sex"] == sex
            ]
            for sex in sexes
        }

        # ----------------------------------------------------
        # График 1. Распределение пациентов по полу
        # ----------------------------------------------------

        ax1 = figure.add_subplot(2, 2, 1)

        ax1.bar(sexes, sex_counts, color="#3b82f6")

        ax1.set_title("Распределение пациентов по полу")
        ax1.set_ylabel("Количество пациентов")
        ax1.tick_params(axis="x", rotation=15)

        # ----------------------------------------------------
        # График 2. Распределение пациентов по возрасту
        # ----------------------------------------------------

        ax2 = figure.add_subplot(2, 2, 2)

        if ages:
            ax2.hist(
                ages,
                bins=10,
                color="#0891b2",
                edgecolor="white"
            )

        ax2.set_title("Распределение пациентов по возрасту")
        ax2.set_xlabel("Возраст, лет")
        ax2.set_ylabel("Количество пациентов")

        # ----------------------------------------------------
        # График 3. Распределение ИМТ с учётом пола
        # ----------------------------------------------------

        ax3 = figure.add_subplot(2, 2, 3)

        box_data = [
            bmi_by_sex[sex]
            for sex in sexes
            if bmi_by_sex[sex]
        ]

        box_labels = [
            sex for sex in sexes
            if bmi_by_sex[sex]
        ]

        if box_data:
            try:
                ax3.boxplot(
                    box_data,
                    tick_labels=box_labels
                )
            except TypeError:
                # Для старых версий Matplotlib
                ax3.boxplot(
                    box_data,
                    labels=box_labels
                )
        else:
            ax3.text(
                0.5, 0.5,
                "Нет данных",
                ha="center",
                va="center"
            )

        ax3.set_title("Распределение ИМТ по полу")
        ax3.set_ylabel("ИМТ")

        # ----------------------------------------------------
        # График 4. Зависимость ИМТ от возраста
        # ----------------------------------------------------

        ax4 = figure.add_subplot(2, 2, 4)

        for sex in sexes:

            group = [
                p for p in patients
                if p["sex"] == sex
            ]

            if group:
                ax4.scatter(
                    [p["age"] for p in group],
                    [p["bmi"] for p in group],
                    label=sex
                )

        if patients:
            ax4.legend()

        ax4.set_title("Зависимость ИМТ от возраста")
        ax4.set_xlabel("Возраст, лет")
        ax4.set_ylabel("ИМТ")

        figure.tight_layout()
        self.canvas.draw()


# ============================================================
# ГЛАВНОЕ ОКНО ПРИЛОЖЕНИЯ
# ============================================================

class FormsView(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Учёт пациентов")
        self.resize(1000, 600)
        self.setMinimumSize(750, 450)

        # Центральный виджет
        central_widget = QWidget()
        central_widget.setObjectName("root")

        self.setCentralWidget(central_widget)

        # Применяем стиль один раз ко всему окну
        self.setStyleSheet(COLD_STYLE)

        # Главный вертикальный макет
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Заголовок
        title = QLabel("Пациенты")
        title.setStyleSheet(
            "font-size: 22px; font-weight: 700; color: #0f172a;"
        )

        layout.addWidget(title)

        # Таблица пациентов
        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "ФИО",
            "Возраст",
            "Пол",
            "Рост, см",
            "Вес, кг",
            "ИМТ"
        ])

        # Запрещаем редактирование ячеек напрямую
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        # Выделение целой строки
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        # Можно выбрать только одного пациента
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        # Внешний вид таблицы
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)

        # Настройка ширины столбцов
        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.ResizeToContents
        )

        self.table.verticalHeader().setDefaultSectionSize(42)

        layout.addWidget(self.table)

        # ----------------------------------------------------
        # Кнопки управления
        # ----------------------------------------------------

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.add_button = QPushButton("Добавить пациента")
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")
        self.stats_button = QPushButton("Статистика")

        # Имена нужны для QSS-селекторов
        self.add_button.setObjectName("addButton")
        self.edit_button.setObjectName("editButton")
        self.delete_button.setObjectName("deleteButton")
        self.stats_button.setObjectName("statsButton")

        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.stats_button)

        layout.addLayout(buttons_layout)

    # ========================================================
    # ОБНОВЛЕНИЕ ТАБЛИЦЫ
    # ========================================================

    def show_patients(self, patients):
        """
        Обновляет содержимое таблицы.

        Стили здесь не задаются и не сбрасываются.
        """

        # Временно отключаем обновление интерфейса,
        # чтобы таблица не перерисовывалась после каждой строки.
        self.table.setUpdatesEnabled(False)

        try:
            self.table.setRowCount(0)

            for patient in patients:

                row = self.table.rowCount()
                self.table.insertRow(row)

                # Формируем ФИО
                full_name = " ".join(
                    part for part in [
                        patient["surname"],
                        patient["name"],
                        patient["patronymic"]
                    ]
                    if part
                )

                values = [
                    full_name,
                    str(patient["age"]),
                    patient["sex"],
                    f"{patient['height_cm']:.1f}",
                    f"{patient['weight_kg']:.1f}",
                    f"{patient['bmi']:.2f}"
                ]

                for column, value in enumerate(values):

                    item = QTableWidgetItem(value)

                    if column == 0:
                        item.setTextAlignment(
                            Qt.AlignmentFlag.AlignVCenter |
                            Qt.AlignmentFlag.AlignLeft
                        )

                        # Сохраняем ID пациента в первой ячейке
                        item.setData(
                            Qt.ItemDataRole.UserRole,
                            patient["id"]
                        )

                    else:
                        item.setTextAlignment(
                            Qt.AlignmentFlag.AlignCenter
                        )

                    self.table.setItem(row, column, item)

            self.table.resizeColumnsToContents()

        finally:
            # Обязательно включаем обновление обратно
            self.table.setUpdatesEnabled(True)
            self.table.viewport().update()

    # ========================================================
    # ВЫБОР ПАЦИЕНТА
    # ========================================================

    def get_selected_patient_id(self):

        row = self.table.currentRow()

        if row < 0:
            return None

        item = self.table.item(row, 0)

        if item is None:
            return None

        return item.data(Qt.ItemDataRole.UserRole)

    # ========================================================
    # ОКНО ДОБАВЛЕНИЯ / РЕДАКТИРОВАНИЯ
    # ========================================================

    def open_patient_dialog(self, patient=None):

        dialog = PatientDialog(patient, self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.get_data()

        return None

    # ========================================================
    # ОКНО СТАТИСТИКИ
    # ========================================================

    def show_statistics(self, patients):

        dialog = StatisticsDialog(patients, self)
        dialog.exec()

    # ========================================================
    # ПОДТВЕРЖДЕНИЕ УДАЛЕНИЯ
    # ========================================================

    def confirm_delete(self):

        answer = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы действительно хотите удалить выбранного пациента?",

            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No,

            QMessageBox.StandardButton.No
        )

        return answer == QMessageBox.StandardButton.Yes

    # ========================================================
    # СООБЩЕНИЯ
    # ========================================================

    def show_error(self, message):

        QMessageBox.critical(
            self,
            "Ошибка",
            message
        )

    def show_info(self, message):

        QMessageBox.information(
            self,
            "Информация",
            message
        )
