from __future__ import annotations

from pathlib import Path

from tinyml_signal_analyzer.data import generate_dataset
from tinyml_signal_analyzer.features import extract_features
from tinyml_signal_analyzer.pipeline import export_model_header, run_training_pipeline


def test_dataset_generation_balanced() -> None:
    dataset = generate_dataset(window_size=128, sample_count=200, seed=7)
    labels = [sample.label for sample in dataset]
    assert labels.count(0) > 70
    assert labels.count(1) > 70


def test_feature_dimension() -> None:
    dataset = generate_dataset(window_size=64, sample_count=20, seed=1)
    feature = extract_features(dataset[0].signal)
    assert len(feature) == 6


def test_pipeline_accuracy() -> None:
    artifact = run_training_pipeline(window_size=128, sample_count=600, seed=42)
    assert artifact.test_accuracy >= 0.92


def test_export_header(tmp_path: Path) -> None:
    artifact = run_training_pipeline(window_size=96, sample_count=300, seed=9)
    output = tmp_path / "tinyml_model_params.h"
    export_model_header(artifact, output)

    content = output.read_text(encoding="utf-8")
    assert "#define TINYML_FEATURE_COUNT" in content
    assert "kTinyMlWeightsQ7" in content
