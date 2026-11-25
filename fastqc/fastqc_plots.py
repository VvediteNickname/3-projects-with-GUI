import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sequences import FastqReader


def _gc_content(dna):
    dna = dna.upper()
    if not dna:
        return 0.0
    gc = sum(1 for ch in dna if ch in ("G", "C"))
    return gc / len(dna) * 100


def plot_per_base_quality(reader, out_path="plot_per_base_quality.png"):
    positions = {}
    for _, _, qual in reader.read():
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


def plot_per_sequence_quality(reader, out_path="plot_per_sequence_quality.png"):
    means = []
    for _, _, qual in reader.read():
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


def plot_per_base_content(reader, out_path="plot_per_base_content.png"):
    positions = {}
    for _, dna, _ in reader.read():
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


def plot_gc_distribution(reader, out_path="plot_gc_distribution.png"):
    gcs = [_gc_content(dna) for _, dna, _ in reader.read()]
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


def plot_length_distribution(reader, out_path="plot_length_distribution.png"):
    lengths = [len(dna) for _, dna, _ in reader.read()]
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


def build_all_plots(reader, out_dir="."):
    results = []

    plots = [
        ("Per base sequence quality", plot_per_base_quality, "plot_per_base_quality.png"),
        ("Per sequence quality scores", plot_per_sequence_quality, "plot_per_sequence_quality.png"),
        ("Per base sequence content", plot_per_base_content, "plot_per_base_content.png"),
        ("Per sequence GC content", plot_gc_distribution, "plot_gc_distribution.png"),
        ("Sequence length distribution", plot_length_distribution, "plot_length_distribution.png"),
    ]

    for title, func, fname in plots:
        out = os.path.join(out_dir, fname)
        try:
            func(reader, out)
            results.append((title, out))
        except Exception as e:
            results.append((title, f"Ошибка: {e}"))

    return results