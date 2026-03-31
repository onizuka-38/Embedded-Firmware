from __future__ import annotations

import math
from collections.abc import Sequence


def _mean(values: Sequence[float]) -> float:
    return sum(values) / float(len(values))


def _std(values: Sequence[float], mean_value: float) -> float:
    variance = sum((value - mean_value) ** 2 for value in values) / float(len(values))
    return math.sqrt(variance)


def extract_features(window: Sequence[float]) -> tuple[float, ...]:
    if len(window) < 4:
        raise ValueError("window must contain at least 4 values")

    mean_value = _mean(window)
    std_value = _std(window, mean_value)
    energy = sum(value * value for value in window) / float(len(window))
    abs_mean = sum(abs(value) for value in window) / float(len(window))
    peak_to_peak = max(window) - min(window)

    zero_crossings = 0
    for idx in range(1, len(window)):
        prev = window[idx - 1]
        curr = window[idx]
        if prev == 0.0:
            continue
        if (prev < 0.0 and curr > 0.0) or (prev > 0.0 and curr < 0.0):
            zero_crossings += 1

    return (
        mean_value,
        std_value,
        energy,
        abs_mean,
        peak_to_peak,
        float(zero_crossings) / float(len(window)),
    )


def normalize_features(
    rows: Sequence[tuple[float, ...]],
    means: tuple[float, ...],
    stds: tuple[float, ...],
) -> list[tuple[float, ...]]:
    if not rows:
        raise ValueError("rows must not be empty")

    normalized: list[tuple[float, ...]] = []
    for row in rows:
        if len(row) != len(means):
            raise ValueError("feature size mismatch")
        normalized.append(
            tuple((value - means[idx]) / stds[idx] for idx, value in enumerate(row))
        )
    return normalized


def fit_normalizer(
    rows: Sequence[tuple[float, ...]],
) -> tuple[tuple[float, ...], tuple[float, ...]]:
    if not rows:
        raise ValueError("rows must not be empty")

    width = len(rows[0])
    if width == 0:
        raise ValueError("rows must have at least one feature")

    sums = [0.0] * width
    for row in rows:
        if len(row) != width:
            raise ValueError("inconsistent feature width")
        for idx, value in enumerate(row):
            sums[idx] += value

    means = tuple(value / float(len(rows)) for value in sums)

    std_values: list[float] = []
    for idx in range(width):
        variance = sum((row[idx] - means[idx]) ** 2 for row in rows) / float(len(rows))
        std_value = math.sqrt(variance)
        std_values.append(std_value if std_value > 1e-6 else 1.0)

    return means, tuple(std_values)
