import os

from sequences import FastaReader, FastqReader
from fastqc_plots import build_all_plots


FASTA_EXTS = (".fasta", ".fa", ".fna")
FASTQ_EXTS = (".fastq", ".fq")


def _pick_reader(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in FASTA_EXTS:
        return FastaReader(path)
    if ext in FASTQ_EXTS:
        return FastqReader(path)
    raise ValueError(f"Неизвестный формат файла: {ext}")


def run_cli(path):
    if not os.path.exists(path):
        print(f"Ошибка: файл не найден: {path}")
        return

    try:
        reader = _pick_reader(path)
    except ValueError as e:
        print(f"Ошибка: {e}")
        return

    count = reader.get_sequences_count()
    avg = reader.get_average_length()

    print(f"Файл: {path}")
    print(f"Число последовательностей: {count}")
    print(f"Средняя длина: {avg:.2f}")
    print()

    print("Графики:")
    for title, result in build_all_plots(reader):
        print(f"  - {title}: {result}")