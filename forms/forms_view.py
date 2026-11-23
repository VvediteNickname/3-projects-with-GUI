from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit, QComboBox,
    QSpinBox, QDoubleSpinBox, QCheckBox,
    QMessageBox, QDialogButtonBox, QLabel, QHeaderView
)
from PySide6.QtCore import Qt

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg


#_everywhere стиль: применяется к окну и наследуется всеми диалогами (parent=self)
COLD_STYLE = """
QWidget { font-size: 13px; color: #0f172a; }
QDialog { background-color: #f4f7fb; }
#root { background-color: #eef2f6; }
QLabel { color: #334155; background: transparent; }

QPushButton {
    background-color: #ffffff; color: #334155;
    border: 1px solid #cbd5e1; border-radius: 10px;
    padding: 9px 18px; font-weight: 600;
}
QPushButton:hover { background-color: #f1f5f9; }
QPushButton:pressed { background-color: #e2e8f0; }

#addButton { background-color: #2563eb; color: white; border: none; }
#addButton:hover { background-color: #1d4ed8; }
#addButton:pressed { background-color: #1e40af; }
#editButton { background-color: #0891b2; color: white; border: none; }
#editButton:hover { background-color: #0e7490; }
#editButton:pressed { background-color: #155e75; }
#deleteButton { background-color: #e11d48; color: white; border: none; }
#deleteButton:hover { background-color: #be123c; }
#deleteButton:pressed { background-color: #9f1239; }
#statsButton { background-color: #475569; color: white; border: none; }
#statsButton:hover { background-color: #334155; }
#statsButton:pressed { background-color: #1e293b; }

QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background-color: #ffffff; border: 1px solid #cbd5e1;
    border-radius: 8px; padding: 6px 10px;
    selection-background-color: #2563eb; selection-color: #ffffff;
}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border: 1px solid #2563eb;
}
QLineEdit:disabled { background-color: #e2e8f0; color: #94a3b8; }

QSpinBox::up-button, QDoubleSpinBox::up-button {
    subcontrol-origin: border; subcontrol-position: top right;
    width: 20px; background: #f1f5f9;
    border-left: 1px solid #cbd5e1; border-top-right-radius: 8px;
}
QSpinBox::down-button, QDoubleSpinBox::down-button {
    subcontrol-origin: border; subcontrol-position: bottom right;
    width: 20px; background: #f1f5f9;
    border-left: 1px solid #cbd5e1; border-bottom-right-radius: 8px;
}
QComboBox::drop-down { border: none; width: 22px; }
QComboBox QAbstractItemView {
    background: #ffffff; border: 1px solid #cbd5e1;
    selection-background-color: #dbeafe; selection-color: #1e3a8a;
}

QCheckBox { spacing: 8px; }
QCheckBox::indicator {
    width: 18px; height: 18px; background: #ffffff;
    border: 1px solid #cbd5e1; border-radius: 5px;
}
QCheckBox::indicator:checked { background-color: #2563eb; border-color: #2563eb; }

QTableWidget {
    background-color: #ffffff; alternate-background-color: #f1f5f9;
    border: 1px solid #cbd5e1; border-radius: 12px;
    gridline-color: transparent;
}
QTableWidget::item { padding: 6px; }
QTableWidget::item:selected { background-color: #dbeafe; color: #1e3a8a; }
QHeaderView::section {
    background-color: #e2e8f0; color: #334155;
    padding: 8px 6px; border: none; font-weight: 600;
}

QScrollBar:vertical { background: #eef2f6; width: 10px; margin: 2px; border-radius: 5px; }
QScrollBar::handle:vertical { background: #94a3b8; border-radius: 5px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: #64748b; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: #eef2f6; height: 10px; margin: 2px; border-radius: 5px; }
QScrollBar::handle:horizontal { background: #94a3b8; border-radius: 5px; min-width: 30px; }
QScrollBar::handle:horizontal:hover { background: #64748b; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

QDialogButtonBox QPushButton { min-width: 90px; }
"""


class PatientDialog(QDialog):

    def __init__(self, patient=None, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Информация о пациенте")
        self.setMinimumWidth(350)

        layout = QFormLayout(self)

        # ФИО
        self.surname_input = QLineEdit()
        self.name_input = QLineEdit()
        self.patronymic_input = QLineEdit()

        self.no_patronymic = QCheckBox("Отчества нет")
        self.no_patronymic.toggled.connect(
            self.patronymic_input.setDisabled
        )

        layout.addRow("Фамилия:", self.surname_input)
        layout.addRow("Имя:", self.name_input)
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

        # Заполнение формы при редактировании
        if patient:
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
        return {
            "surname": self.surname_input.text().strip(),
            "name": self.name_input.text().strip(),
            "patronymic": (
                "" if self.no_patronymic.isChecked()
                else self.patronymic_input.text().strip()
            ),
            "sex": self.sex_input.currentText(),
            "age": self.age_input.value(),
            "height_cm": self.height_input.value(),
            "weight_kg": self.weight_input.value()
        }


class StatisticsDialog(QDialog):

    def __init__(self, patients, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Статистика пациентов")
        self.resize(1000, 750)

        layout = QVBoxLayout(self)

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

        # График 1. Распределение по полу
        ax1 = figure.add_subplot(2, 2, 1)
        ax1.bar(sexes, sex_counts)
        ax1.set_title("Распределение пациентов по полу")
        ax1.set_ylabel("Количество пациентов")
        ax1.tick_params(axis="x", rotation=15)

        # График 2. Распределение по возрасту
        ax2 = figure.add_subplot(2, 2, 2)

        if ages:
            ax2.hist(ages, bins=10, edgecolor="black")

        ax2.set_title("Распределение пациентов по возрасту")
        ax2.set_xlabel("Возраст, лет")
        ax2.set_ylabel("Количество пациентов")

        # График 3. ИМТ с учётом пола
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
            ax3.boxplot(box_data, tick_labels=box_labels)
        else:
            ax3.text(0.5, 0.5, "Нет данных", ha="center")

        ax3.set_title("Распределение ИМТ по полу")
        ax3.set_ylabel("ИМТ")

        # График 4. Зависимость ИМТ от возраста
        ax4 = figure.add_subplot(2, 2, 4)

        if patients:
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

            ax4.legend()

        ax4.set_title("Зависимость ИМТ от возраста")
        ax4.set_xlabel("Возраст, лет")
        ax4.set_ylabel("ИМТ")

        figure.tight_layout()
        self.canvas.draw()


class FormsView(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Учёт пациентов")
        self.resize(1000, 600)

        # Центральный виджет + холодный стиль
        central_widget = QWidget()
        central_widget.setObjectName("root")
        central_widget.setAttribute(Qt.WA_StyledBackground, True)
        self.setCentralWidget(central_widget)
        self.setStyleSheet(COLD_STYLE)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

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

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        # Внешний вид таблицы: зебра, без решётки и номеров строк
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(self.table)

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.add_button = QPushButton("Добавить пациента")
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")
        self.stats_button = QPushButton("Статистика")

        # имена для QSS-селекторов #addButton, #editButton и т.д.
        self.add_button.setObjectName("addButton")
        self.edit_button.setObjectName("editButton")
        self.delete_button.setObjectName("deleteButton")
        self.stats_button.setObjectName("statsButton")

        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.stats_button)

        layout.addLayout(buttons_layout)

    def show_patients(self, patients):
        self.table.setRowCount(0)

        for patient in patients:
            row = self.table.rowCount()
            self.table.insertRow(row)

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
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                if column == 0:
                    item.setData(
                        Qt.ItemDataRole.UserRole,
                        patient["id"]
                    )

                self.table.setItem(row, column, item)

        self.table.resizeColumnsToContents()

    def get_selected_patient_id(self):
        row = self.table.currentRow()

        if row < 0:
            return None

        item = self.table.item(row, 0)

        return item.data(Qt.ItemDataRole.UserRole)

    def open_patient_dialog(self, patient=None):
        dialog = PatientDialog(patient, self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.get_data()

        return None

    def show_statistics(self, patients):
        dialog = StatisticsDialog(patients, self)
        dialog.exec()

    def confirm_delete(self):
        answer = QMessageBox.question(
            self,
            "Подтверждение",
            "Удалить выбранного пациента?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return answer == QMessageBox.StandardButton.Yes

    def show_error(self, message):
        QMessageBox.critical(self, "Ошибка", message)

    def show_info(self, message):
        QMessageBox.information(self, "Информация", message)