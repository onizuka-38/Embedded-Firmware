from __future__ import annotations

from pathlib import Path

from tinyml_signal_analyzer.data import load_measurement_dataset
from tinyml_signal_analyzer.features import extract_features
from tinyml_signal_analyzer.pipeline import export_model_header, run_training_pipeline


def _write_dataset_csv(path: Path, rows: int) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write("signal,label\n")
        for idx in range(rows):
            base = 0.45 if idx % 2 == 0 else -0.45
            if idx >= rows // 2:
                value = base * 1.9
                label = 1
            else:
                value = base
                label = 0
            handle.write(f"{value:.6f},{label}\n")


def test_dataset_loading(tmp_path: Path) -> None:
    csv_path = tmp_path / "vibration.csv"
    _write_dataset_csv(csv_path, rows=320)

    dataset = load_measurement_dataset(tmp_path, window_size=64, stride=16)
    labels = [sample.label for sample in dataset]

    assert len(dataset) > 10
    assert labels.count(0) > 0
    assert labels.count(1) > 0


def test_feature_dimension(tmp_path: Path) -> None:
    csv_path = tmp_path / "ecg.csv"
    _write_dataset_csv(csv_path, rows=200)

    dataset = load_measurement_dataset(tmp_path, window_size=64, stride=16)
    feature = extract_features(dataset[0].signal)
    assert len(feature) == 6


def test_pipeline_accuracy(tmp_path: Path) -> None:
    csv_path = tmp_path / "emg.csv"
    _write_dataset_csv(csv_path, rows=640)

    artifact = run_training_pipeline(dataset_dir=tmp_path, window_size=128, stride=32, seed=42)
    assert artifact.test_accuracy >= 0.80


def test_export_header(tmp_path: Path) -> None:
    csv_path = tmp_path / "machine.csv"
    _write_dataset_csv(csv_path, rows=500)

    artifact = run_training_pipeline(dataset_dir=tmp_path, window_size=96, stride=24, seed=9)
    output = tmp_path / "tinyml_model_params.h"
    export_model_header(artifact, output)

    content = output.read_text(encoding="utf-8")
    assert "#define TINYML_FEATURE_COUNT" in content
    assert "kTinyMlWeightsQ7" in content
