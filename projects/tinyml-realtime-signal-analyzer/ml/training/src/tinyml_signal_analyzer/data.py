from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WindowSample:
    signal: tuple[float, ...]
    label: int


def _majority_label(labels: list[int]) -> int:
    counts: dict[int, int] = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    winner = max(counts.items(), key=lambda item: item[1])
    return winner[0]


def _read_signal_rows(csv_path: Path, signal_key: str, label_key: str) -> list[tuple[float, int]]:
    rows: list[tuple[float, int]] = []
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = {signal_key, label_key} - set(reader.fieldnames or [])
        if missing:
            missing_text = ", ".join(sorted(missing))
            raise ValueError(f"{csv_path}: missing required columns: {missing_text}")

        for row in reader:
            rows.append((float(row[signal_key]), int(row[label_key])))
    return rows


def _windowize(rows: list[tuple[float, int]], window_size: int, stride: int) -> list[WindowSample]:
    if window_size < 16:
        raise ValueError("window_size must be at least 16")
    if stride <= 0:
        raise ValueError("stride must be positive")

    samples: list[WindowSample] = []
    start = 0
    while start + window_size <= len(rows):
        window = rows[start : start + window_size]
        signal = tuple(value for value, _ in window)
        labels = [label for _, label in window]
        samples.append(WindowSample(signal=signal, label=_majority_label(labels)))
        start += stride
    return samples


def load_measurement_dataset(
    data_root: Path,
    window_size: int,
    stride: int,
    signal_column: str = "signal",
    label_column: str = "label",
) -> list[WindowSample]:
    if not data_root.exists():
        raise ValueError(f"dataset path does not exist: {data_root}")

    csv_files = sorted(data_root.rglob("*.csv"))
    if not csv_files:
        raise ValueError(f"no CSV files found under: {data_root}")

    dataset: list[WindowSample] = []
    for csv_path in csv_files:
        rows = _read_signal_rows(csv_path, signal_column, label_column)
        dataset.extend(_windowize(rows=rows, window_size=window_size, stride=stride))

    if len(dataset) < 8:
        raise ValueError("not enough windowed samples; collect more signal data")

    return dataset
