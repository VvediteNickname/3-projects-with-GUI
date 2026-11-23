import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="FastQC-lite: статистика по FASTA/FASTQ"
    )
    parser.add_argument(
        "file", nargs="?", default=None,
        help="Путь к FASTA/FASTQ файлу (для CLI-режима)"
    )
    parser.add_argument(
        "--gui", action="store_true",
        help="Запустить графический интерфейс"
    )
    args = parser.parse_args()

    if args.gui or args.file is None:
        # GUI-режим: либо явно --gui, либо файл не указан
        from fastqc_gui import run_gui
        run_gui(initial_file=args.file)
    else:
        # CLI-режим
        from fastqc_cli import run_cli
        run_cli(args.file)


if __name__ == "__main__":
    main()