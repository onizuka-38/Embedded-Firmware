from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class BinaryMetrics:
    accuracy: float


class LogisticBinaryClassifier:
    def __init__(self, feature_count: int) -> None:
        if feature_count <= 0:
            raise ValueError("feature_count must be positive")
        self._weights: list[float] = [0.0] * feature_count
        self._bias: float = 0.0

    @property
    def weights(self) -> tuple[float, ...]:
        return tuple(self._weights)

    @property
    def bias(self) -> float:
        return self._bias

    @staticmethod
    def _sigmoid(value: float) -> float:
        if value >= 0.0:
            z_pos = math.exp(-value)
            return 1.0 / (1.0 + z_pos)
        z_neg = math.exp(value)
        return z_neg / (1.0 + z_neg)

    def _linear(self, row: Sequence[float]) -> float:
        if len(row) != len(self._weights):
            raise ValueError("feature width mismatch")
        score = self._bias
        for weight, value in zip(self._weights, row, strict=True):
            score += weight * value
        return score

    def predict_proba(self, row: Sequence[float]) -> float:
        return self._sigmoid(self._linear(row))

    def predict(self, row: Sequence[float]) -> int:
        return 1 if self.predict_proba(row) >= 0.5 else 0

    def fit(
        self,
        rows: Sequence[Sequence[float]],
        labels: Sequence[int],
        epochs: int,
        learning_rate: float,
    ) -> None:
        if len(rows) != len(labels):
            raise ValueError("rows and labels must have the same length")
        if epochs <= 0:
            raise ValueError("epochs must be positive")
        if learning_rate <= 0.0:
            raise ValueError("learning_rate must be positive")

        sample_count = len(rows)
        for _ in range(epochs):
            grad_weights = [0.0] * len(self._weights)
            grad_bias = 0.0
            for row, label in zip(rows, labels, strict=True):
                prediction = self.predict_proba(row)
                error = prediction - float(label)
                for idx, value in enumerate(row):
                    grad_weights[idx] += error * value
                grad_bias += error

            scale = learning_rate / float(sample_count)
            for idx in range(len(self._weights)):
                self._weights[idx] -= scale * grad_weights[idx]
            self._bias -= scale * grad_bias

    def evaluate(self, rows: Sequence[Sequence[float]], labels: Sequence[int]) -> BinaryMetrics:
        if len(rows) != len(labels):
            raise ValueError("rows and labels must have the same length")
        correct = 0
        for row, label in zip(rows, labels, strict=True):
            if self.predict(row) == label:
                correct += 1
        return BinaryMetrics(accuracy=correct / float(len(rows)))
