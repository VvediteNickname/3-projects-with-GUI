
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit, QComboBox,
    QSpinBox, QDoubleSpinBox, QCheckBox,
    QMessageBox, QDialogButtonBox, QLabel
)
from PySide6.QtCore import Qt

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg


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

        bmi = [p["bmi"] for p in patients]

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

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

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

        layout.addWidget(self.table)

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить пациента")
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")
        self.stats_button = QPushButton("Статистика")

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
            self, "Подтверждение", "Удалить выбранного пациента?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No      # по умолчанию «Нет» — безопасно
        )
        return answer == QMessageBox.StandardButton.Yes


    def show_error(self, message):
        QMessageBox.critical(self, "Ошибка", message)

    def show_info(self, message):
        QMessageBox.information(self, "Информация", message)

