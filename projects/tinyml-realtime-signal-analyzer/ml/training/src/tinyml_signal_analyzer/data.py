from __future__ import annotations

import math
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class WindowSample:
    signal: tuple[float, ...]
    label: int


def _normal_signal(length: int, rng: random.Random) -> tuple[float, ...]:
    values: list[float] = []
    freq = rng.uniform(0.8, 1.2)
    for idx in range(length):
        t = idx / float(length)
        base = math.sin(2.0 * math.pi * freq * t)
        noise = rng.uniform(-0.08, 0.08)
        values.append(base + noise)
    return tuple(values)


def _anomaly_signal(length: int, rng: random.Random) -> tuple[float, ...]:
    values: list[float] = []
    freq = rng.uniform(1.8, 2.4)
    spike_index = rng.randint(length // 4, (3 * length) // 4)
    for idx in range(length):
        t = idx / float(length)
        base = math.sin(2.0 * math.pi * freq * t)
        noise = rng.uniform(-0.10, 0.10)
        spike = 0.0
        if abs(idx - spike_index) <= 1:
            spike = rng.uniform(1.4, 2.0)
        values.append(base + noise + spike)
    return tuple(values)


def generate_dataset(window_size: int, sample_count: int, seed: int) -> list[WindowSample]:
    if window_size < 16:
        raise ValueError("window_size must be at least 16")
    if sample_count < 10:
        raise ValueError("sample_count must be at least 10")

    rng = random.Random(seed)
    dataset: list[WindowSample] = []

    for _ in range(sample_count // 2):
        dataset.append(WindowSample(signal=_normal_signal(window_size, rng), label=0))
        dataset.append(WindowSample(signal=_anomaly_signal(window_size, rng), label=1))

    rng.shuffle(dataset)
    return dataset[:sample_count]
