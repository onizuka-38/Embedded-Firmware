from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from math import exp


@dataclass(frozen=True)
class QuantizedLinearModel:
    weights_q7: tuple[int, ...]
    weight_scale: float
    bias_q7: int


def quantize_q7(values: Sequence[float]) -> tuple[tuple[int, ...], float]:
    if not values:
        raise ValueError("values must not be empty")

    max_abs = max(abs(value) for value in values)
    if max_abs < 1e-8:
        return tuple(0 for _ in values), 1.0

    scale = max_abs / 127.0
    quantized = tuple(max(-127, min(127, int(round(value / scale)))) for value in values)
    return quantized, scale


def quantize_linear_model(weights: Sequence[float], bias: float) -> QuantizedLinearModel:
    weights_q7, weight_scale = quantize_q7(weights)
    bias_q7 = int(round(bias / weight_scale)) if weight_scale > 0.0 else 0
    return QuantizedLinearModel(weights_q7=weights_q7, weight_scale=weight_scale, bias_q7=bias_q7)


def predict_q7(features: Sequence[float], model: QuantizedLinearModel) -> float:
    if len(features) != len(model.weights_q7):
        raise ValueError("feature width mismatch")

    acc = model.bias_q7
    for value, weight in zip(features, model.weights_q7, strict=True):
        acc += int(round(value / model.weight_scale)) * weight

    dequantized = float(acc) * model.weight_scale * model.weight_scale
    if dequantized >= 0.0:
        return 1.0 / (1.0 + exp(-dequantized))
    z_neg = exp(dequantized)
    return z_neg / (1.0 + z_neg)
