
import json
import uuid
from pathlib import Path


class FormsModel:

    def __init__(self):
        # Папка для файлов пациентов
        self.data_folder = Path(__file__).parent / "data" / "patients"
        self.data_folder.mkdir(parents=True, exist_ok=True)

        # Загружаем пациентов при создании модели
        self.patients = self.load_patients()

    def calculate_bmi(self, height_cm, weight_kg):
        # Переводим рост из сантиметров в метры
        height_m = height_cm / 100

        if height_m <= 0:
            raise ValueError("Рост должен быть больше нуля")

        return weight_kg / (height_m ** 2)

    def validate_patient(self, data):
        if not data["surname"].strip():
            raise ValueError("Введите фамилию")

        if not data["name"].strip():
            raise ValueError("Введите имя")

        if data["age"] < 0:
            raise ValueError("Возраст не может быть отрицательным")

        if data["height_cm"] <= 0:
            raise ValueError("Рост должен быть больше нуля")

        if data["weight_kg"] <= 0:
            raise ValueError("Вес должен быть больше нуля")

    def add_patient(self, data):
        self.validate_patient(data)

        patient = data.copy()
        patient["id"] = str(uuid.uuid4())
        patient["bmi"] = self.calculate_bmi(
            patient["height_cm"],
            patient["weight_kg"]
        )

        self.patients.append(patient)
        self.save_patient(patient)

    def update_patient(self, patient_id, data):
        self.validate_patient(data)

        for index, patient in enumerate(self.patients):
            if patient["id"] == patient_id:

                updated_patient = data.copy()
                updated_patient["id"] = patient_id
                updated_patient["bmi"] = self.calculate_bmi(
                    updated_patient["height_cm"],
                    updated_patient["weight_kg"]
                )

                self.patients[index] = updated_patient
                self.save_patient(updated_patient)
                return

        raise ValueError("Пациент не найден")

    def save_patient(self, patient):
        file_path = self.data_folder / f"{patient['id']}.json"

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(patient, file, ensure_ascii=False, indent=4)

    def load_patients(self):
        patients = []

        for file_path in self.data_folder.glob("*.json"):
            with open(file_path, "r", encoding="utf-8") as file:
                patient = json.load(file)

            # Пересчитываем ИМТ при загрузке
            patient["bmi"] = self.calculate_bmi(
                patient["height_cm"],
                patient["weight_kg"]
            )

            patients.append(patient)

        return patients

    def get_patients(self):
        return self.patients

