import os
from sequences import FastqReader
from fastqc_plots import build_all_plots


def run_cli(path):
    if not os.path.exists(path):
        print(f"Ошибка: файл не найден: {path}")
        return

    if not path.lower().endswith((".fastq", ".fq")):
        print("Ошибка: поддерживаются только FASTQ (*.fastq, *.fq)")
        return

    reader = FastqReader(path)

    count = reader.get_sequences_count()
    avg = reader.get_average_length()

    print(f"Файл: {path}")
    print(f"Число последовательностей: {count}")
    print(f"Средняя длина: {avg:.2f}")
    print()

    print("Графики:")
    for title, result in build_all_plots(reader):
        print(f"  - {title}: {result}")