from __future__ import annotations

import math

from tinyml_signal_analyzer.features import extract_features


def _c_equivalent_extract(window: list[float]) -> tuple[float, ...]:
    n = len(window)
    if n < 4:
        raise ValueError("window size must be >= 4")

    value_sum = 0.0
    abs_sum = 0.0
    energy_sum = 0.0
    min_value = window[0]
    max_value = window[0]
    zero_crossings = 0

    for idx, value in enumerate(window):
        value_sum += value
        abs_sum += abs(value)
        energy_sum += value * value

        if value < min_value:
            min_value = value
        if value > max_value:
            max_value = value

        if idx > 0:
            prev = window[idx - 1]
            if (prev < 0.0 and value > 0.0) or (prev > 0.0 and value < 0.0):
                zero_crossings += 1

    inv_n = 1.0 / float(n)
    mean = value_sum * inv_n

    variance_sum = 0.0
    for value in window:
        diff = value - mean
        variance_sum += diff * diff

    return (
        mean,
        math.sqrt(variance_sum * inv_n),
        energy_sum * inv_n,
        abs_sum * inv_n,
        max_value - min_value,
        float(zero_crossings) * inv_n,
    )


def test_feature_parity_with_c_equivalent() -> None:
    window = [
        -0.8,
        -0.4,
        -0.1,
        0.2,
        0.5,
        0.7,
        0.1,
        -0.2,
        -0.6,
        0.4,
        0.9,
        -0.3,
    ]

    py_features = extract_features(window)
    c_features = _c_equivalent_extract(window)

    assert len(py_features) == len(c_features)
    for py_value, c_value in zip(py_features, c_features, strict=True):
        assert abs(py_value - c_value) < 1e-9
