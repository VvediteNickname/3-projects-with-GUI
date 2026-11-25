# FastQC-lite GUI Projects

Три учебных проекта на **PySide6** с графическим интерфейсом: калькулятор, база пациентов и анализатор биологических последовательностей. Все программы построены по архитектуре MVC и используют единый подход к стилизации через QSS.

---

## Быстрый старт (одна команда)

```bash
git clone https://github.com/VvediteNickname/3-projects-with-GUI.git
cd 3-projects-with-GUI
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# .\venv\Scripts\activate       # Windows (PowerShell)
pip install -r requirements.txt
```

Проверка, что всё работает:

```bash
python calculator/src/main.py      # калькулятор
python forms/forms_main.py         # пациенты
python fastqc/main.py              # FastQC (GUI)
python fastqc/main.py fastqc/sample.fastq   # FastQC (CLI)
```

> **Windows:** в PowerShell активация venv — `.\venv\Scripts\activate`.  
> В cmd — `venv\Scripts\activate.bat`.  
> Если PowerShell ругается на политику выполнения:  
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

---

## Проекты

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

Проверить версию Python:

```bash
python3 --version    # Linux / macOS
python --version     # Windows
```

Если версия ниже 3.10 — обновите Python или используйте [pyenv](https://github.com/pyenv/pyenv).

---

## Установка зависимостей

Все зависимости собраны в `requirements.txt`:

```
PySide6
matplotlib
```

Установка одной командой (после активации venv):

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Linux (Ubuntu/Debian)

Если `python3 -m venv` не срабатывает — доустановите пакет:

```bash
sudo apt install python3-venv
```

Для PySide6 могут понадобиться системные библиотеки:

```bash
sudo apt install libxcb-cursor0 libxkbcommon-x11-0
```

### Fedora

```bash
sudo dnf install python3-devel xcb-util-cursor
```

### macOS

```bash
brew install python@3.12
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
├── requirements.txt
└── README.md
```

---

## Если что-то пошло не так

**`ModuleNotFoundError: No module named 'PySide6'`**  
— venv не активирован. Активируйте (`source venv/bin/activate` или `.\venv\Scripts\activate`) и повторите `pip install -r requirements.txt`.

**`qt.qpa.plugin: Could not load the Qt platform plugin "xcb"`**  
— не хватает системных библиотек. На Ubuntu/Debian:  
`sudo apt install libxcb-cursor0 libxkbcommon-x11-0`

**`ImportError: libGL.so.1: cannot open shared object file`**  
— на минимальных Linux-образах:  
`sudo apt install libgl1`

**PowerShell не даёт активировать venv**  
— выполните один раз:  
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

**FastQC: `graphviz` / `matplotlib` не рисует**  
— проверьте, что `matplotlib` установлен: `pip show matplotlib`. Если нет — `pip install matplotlib`.

---

## Лицензия

Учебный проект. Код открыт для изучения и адаптации.