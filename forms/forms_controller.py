
class FormsController:

    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Подключаем кнопки к обработчикам
        self.view.add_button.clicked.connect(self.add_patient)
        self.view.edit_button.clicked.connect(self.edit_patient)
        self.view.stats_button.clicked.connect(self.show_statistics)

        # Показываем загруженных пациентов
        self.update_table()

    def update_table(self):
        patients = self.model.get_patients()
        self.view.show_patients(patients)

    def add_patient(self):
        data = self.view.open_patient_dialog()

        if data is None:
            return

        try:
            self.model.add_patient(data)
            self.update_table()
            self.view.show_info("Пациент успешно добавлен")

        except (ValueError, OSError) as error:
            self.view.show_error(str(error))

    def edit_patient(self):
        patient_id = self.view.get_selected_patient_id()

        if patient_id is None:
            self.view.show_error("Сначала выберите пациента в таблице")
            return

        patient = next(
            (
                p for p in self.model.get_patients()
                if p["id"] == patient_id
            ),
            None
        )

        if patient is None:
            self.view.show_error("Пациент не найден")
            return

        data = self.view.open_patient_dialog(patient)

        if data is None:
            return

        try:
            self.model.update_patient(patient_id, data)
            self.update_table()
            self.view.show_info("Данные пациента обновлены")

        except (ValueError, OSError) as error:
            self.view.show_error(str(error))

    def show_statistics(self):
        patients = self.model.get_patients()

        if not patients:
            self.view.show_error("Пока нет данных для статистики")
            return

        self.view.show_statistics(patients)

