from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

from .data import WindowSample, load_measurement_dataset
from .features import extract_features, fit_normalizer, normalize_features
from .model import LogisticBinaryClassifier
from .quantization import QuantizedLinearModel, quantize_linear_model


@dataclass(frozen=True)
class TrainingArtifact:
    feature_means: tuple[float, ...]
    feature_stds: tuple[float, ...]
    weights: tuple[float, ...]
    bias: float
    quantized_model: QuantizedLinearModel
    test_accuracy: float


def _split_dataset(
    dataset: list[WindowSample],
    train_ratio: float,
) -> tuple[list[WindowSample], list[WindowSample]]:
    split = int(len(dataset) * train_ratio)
    return dataset[:split], dataset[split:]


def run_training_pipeline(
    dataset_dir: Path,
    window_size: int = 128,
    stride: int = 32,
    seed: int = 42,
) -> TrainingArtifact:
    dataset = load_measurement_dataset(
        data_root=dataset_dir,
        window_size=window_size,
        stride=stride,
    )

    random.Random(seed).shuffle(dataset)
    train_set, test_set = _split_dataset(dataset, train_ratio=0.8)

    train_features = [extract_features(sample.signal) for sample in train_set]
    test_features = [extract_features(sample.signal) for sample in test_set]

    feature_means, feature_stds = fit_normalizer(train_features)
    train_x = normalize_features(train_features, feature_means, feature_stds)
    test_x = normalize_features(test_features, feature_means, feature_stds)

    train_y = [sample.label for sample in train_set]
    test_y = [sample.label for sample in test_set]

    classifier = LogisticBinaryClassifier(feature_count=len(train_x[0]))
    classifier.fit(train_x, train_y, epochs=300, learning_rate=0.25)

    metrics = classifier.evaluate(test_x, test_y)
    quantized = quantize_linear_model(classifier.weights, classifier.bias)

    return TrainingArtifact(
        feature_means=feature_means,
        feature_stds=feature_stds,
        weights=classifier.weights,
        bias=classifier.bias,
        quantized_model=quantized,
        test_accuracy=metrics.accuracy,
    )


def export_model_header(artifact: TrainingArtifact, path: Path) -> None:
    lines: list[str] = []
    lines.append("#ifndef TINYML_MODEL_PARAMS_H")
    lines.append("#define TINYML_MODEL_PARAMS_H")
    lines.append("")
    lines.append("#include <stdint.h>")
    lines.append("")
    lines.append(f"#define TINYML_FEATURE_COUNT ({len(artifact.weights)})")
    lines.append(f"#define TINYML_WEIGHT_SCALE ({artifact.quantized_model.weight_scale:.10f}f)")
    lines.append(f"#define TINYML_BIAS_Q7 ({artifact.quantized_model.bias_q7})")
    lines.append("")

    weights_str = ", ".join(str(value) for value in artifact.quantized_model.weights_q7)
    means_str = ", ".join(f"{value:.10f}f" for value in artifact.feature_means)
    stds_str = ", ".join(f"{value:.10f}f" for value in artifact.feature_stds)

    lines.append(f"static const int8_t kTinyMlWeightsQ7[TINYML_FEATURE_COUNT] = {{{weights_str}}};")
    lines.append(f"static const float kTinyMlFeatureMeans[TINYML_FEATURE_COUNT] = {{{means_str}}};")
    lines.append(f"static const float kTinyMlFeatureStds[TINYML_FEATURE_COUNT] = {{{stds_str}}};")
    lines.append("")
    lines.append("#endif")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
