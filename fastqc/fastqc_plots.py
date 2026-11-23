import os
import matplotlib
matplotlib.use("Agg")           # без GUI-бэкенда, чтобы работало и в CLI, и в GUI
import matplotlib.pyplot as plt

from sequences import FastaReader, FastqReader


def _iter_records(reader):
    """Единый итератор: для FASTA вернёт (name, dna, None), для FASTQ (name, dna, qual)."""
    for item in reader.read():
        if len(item) == 3:
            yield item[0], item[1], item[2]
        else:
            yield item[0], item[1], None


def _gc_content(dna):
    dna = dna.upper()
    if not dna:
        return 0.0
    gc = sum(1 for ch in dna if ch in ("G", "C"))
    return gc / len(dna) * 100


# ---------- 1. качество по позициям (у тебя уже есть, оставим совместимость) ----------

def plot_per_base_quality(reader, out_path="plot_per_base_quality.png"):
    """Среднее качество по позициям. Только FASTQ."""
    positions = {}
    for _, _, qual in _iter_records(reader):
        if qual is None:
            raise ValueError("График качества доступен только для FASTQ")
        for i, ch in enumerate(qual):
            positions.setdefault(i, []).append(ord(ch) - 33)

    if not positions:
        raise ValueError("Нет данных о качестве")

    xs = sorted(positions.keys())
    ys = [sum(positions[i]) / len(positions[i]) for i in xs]

    plt.figure()
    plt.plot(xs, ys, color="blue")
    plt.title("Per base sequence quality")
    plt.xlabel("Позиция")
    plt.ylabel("Среднее качество")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return out_path


# ---------- 2. распределение среднего качества по прочтениям ----------

def plot_per_sequence_quality(reader, out_path="plot_per_sequence_quality.png"):
    """Гистограмма среднего качества каждой последовательности. Только FASTQ."""
    means = []
    for _, _, qual in _iter_records(reader):
        if qual is None:
            raise ValueError("График качества доступен только для FASTQ")
        if not qual:
            continue
        scores = [ord(ch) - 33 for ch in qual]
        means.append(sum(scores) / len(scores))

    if not means:
        raise ValueError("Нет данных о качестве")

    plt.figure()
    plt.hist(means, bins=20, color="steelblue", edgecolor="black")
    plt.title("Per sequence quality scores")
    plt.xlabel("Среднее качество прочтения")
    plt.ylabel("Число прочтений")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return out_path


# ---------- 3. состав оснований по позициям ----------

def plot_per_base_content(reader, out_path="plot_per_base_content.png"):
    """Доля A/T/G/C по позициям."""
    positions = {}
    for _, dna, _ in _iter_records(reader):
        for i, ch in enumerate(dna.upper()):
            positions.setdefault(i, {"A": 0, "T": 0, "G": 0, "C": 0})
            if ch in positions[i]:
                positions[i][ch] += 1

    if not positions:
        raise ValueError("Нет последовательностей")

    xs = sorted(positions.keys())
    shares = {b: [] for b in "ATGC"}
    for i in xs:
        total = sum(positions[i].values()) or 1
        for b in "ATGC":
            shares[b].append(positions[i][b] / total * 100)

    plt.figure()
    colors = {"A": "green", "T": "red", "G": "blue", "C": "orange"}
    for b in "ATGC":
        plt.plot(xs, shares[b], label=b, color=colors[b])
    plt.title("Per base sequence content")
    plt.xlabel("Позиция")
    plt.ylabel("Доля, %")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return out_path


# ---------- 4. распределение GC-content ----------

def plot_gc_distribution(reader, out_path="plot_gc_distribution.png"):
    """Гистограмма GC-content по последовательностям."""
    gcs = [_gc_content(dna) for _, dna, _ in _iter_records(reader)]
    if not gcs:
        raise ValueError("Нет последовательностей")

    plt.figure()
    plt.hist(gcs, bins=20, color="seagreen", edgecolor="black")
    plt.title("Per sequence GC content")
    plt.xlabel("GC, %")
    plt.ylabel("Число последовательностей")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return out_path


# ---------- 5. распределение длин ----------

def plot_length_distribution(reader, out_path="plot_length_distribution.png"):
    """Гистограмма длин последовательностей."""
    lengths = [len(dna) for _, dna, _ in _iter_records(reader)]
    if not lengths:
        raise ValueError("Нет последовательностей")

    plt.figure()
    plt.hist(lengths, bins=20, color="purple", edgecolor="black")
    plt.title("Sequence length distribution")
    plt.xlabel("Длина")
    plt.ylabel("Число последовательностей")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return out_path


# ---------- удобная обёртка ----------

def build_all_plots(reader, out_dir="."):
    """Строит все доступные графики, возвращает список путей.

    Для FASTQ — 5 графиков, для FASTA — 3 (без качества).
    Ошибки по отдельным графикам не валят остальные.
    """
    results = []

    # общие для FASTA/FASTQ
    common = [
        ("Per base sequence content", plot_per_base_content, "plot_per_base_content.png"),
        ("Per sequence GC content",   plot_gc_distribution,  "plot_gc_distribution.png"),
        ("Sequence length distribution", plot_length_distribution, "plot_length_distribution.png"),
    ]

    # только FASTQ
    fastq_only = [
        ("Per base sequence quality", plot_per_base_quality, "plot_per_base_quality.png"),
        ("Per sequence quality scores", plot_per_sequence_quality, "plot_per_sequence_quality.png"),
    ]

    plots = list(common)
    if isinstance(reader, FastqReader):
        plots += fastq_only

    for title, func, fname in plots:
        out = os.path.join(out_dir, fname)
        try:
            func(reader, out)
            results.append((title, out))
        except Exception as e:
            results.append((title, f"Ошибка: {e}"))

    return results