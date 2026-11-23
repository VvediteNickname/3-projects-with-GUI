# FastQC-lite GUI Projects 🧬

Три учебных проекта на **PySide6** с графическим интерфейсом: калькулятор, база пациентов и анализатор биологических последовательностей. Все программы построены по архитектуре MVC и используют единый подход к стилизации через QSS.

---

## 📋 Проекты

### 1. Calculator
Калькулятор с поддержкой операций `+ − × ÷`, квадратного корня и клавиатуры. Архитектура MVC: модель хранит только математику, view — кнопки и стили, controller связывает их через словарь колбэков.

**Запуск:**
```bash
python calculator/src/main.py
```

### 2. Forms
Приложение для учёта пациентов: добавление, редактирование, удаление, просмотр статистики. Данные хранятся в JSON-файлах (каждый пациент — отдельный файл в `forms/data/patients/`), ИМТ рассчитывается автоматически. Статистика включает 4 графика (matplotlib) — распределение по полу, возрасту, ИМТ, зависимость ИМТ от возраста.

**Запуск:**
```bash
python forms/forms_main.py
```

### 3. FastQC-lite
Анализатор биологических последовательностей в форматах **FASTA** и **FASTQ**. Поддерживает:
- чтение через генераторы (экономия памяти);
- drag&drop файлов в окно;
- 5 графиков качества для FASTQ и 3 для FASTA;
- два режима запуска — GUI и CLI.

**Запуск GUI:**
```bash
python fastqc/main.py
# или явно
python fastqc/main.py --gui
```

**Запуск CLI:**
```bash
python fastqc/main.py путь/к/файлу.fastq
```

---

## 🛠 Требования

- **Python 3.10** и новее (тестировалось на 3.12 и 3.14)
- **pip** для установки зависимостей

---

## Установка зависимостей

### Linux (Ubuntu, Debian, Fedora, Arch, macOS)

```bash
cd ~/3-projects-with-GUI   # путь к твоей папке

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install PySide6 matplotlib numpy
```


---

### Windows

```powershell
cd C:\Users\ТвойЮзер\3-projects-with-GUI

python -m venv venv
.\venv\Scripts\activate

pip install --upgrade pip
pip install PySide6 matplotlib numpy
```

---

## Быстрый старт

```bash
# Калькулятор
python calculator/src/main.py

# Форма пациентов
python forms/forms_main.py

# FastQC (GUI)
python fastqc/main.py

# FastQC (CLI, пример)
python fastqc/main.py fastqc/sample.fastq
```

---

## Структура проекта

```
3-projects-with-GUI/
├── calculator/
│   └── src/
│       ├── main.py          # точка входа
│       ├── model.py         # математика
│       ├── view.py          # PySide6 окно
│       └── controller.py    # логика
├── forms/
│   ├── data/patients/       # JSON-файлы пациентов
│   ├── forms_main.py        # точка входа
│   ├── forms_model.py       # работа с данными
│   ├── forms_view.py        # таблицы, диалоги, графики
│   └── forms_controller.py  # логика
├── fastqc/
│   ├── main.py              # точка входа (CLI/GUI)
│   ├── fastqc_gui.py        # окно FastQC
│   ├── fastqc_cli.py        # консольный режим
│   ├── sequences.py         # чтение FASTA/FASTQ
│   ├── fastqc_plots.py      # построение графиков
│   ├── reader.py            # базовый класс чтения
│   └── sample.fastq         # пример файла
└── README.md
```

---

## 📝 Лицензия

Учебный проект. Код открыт для изучения и адаптации.