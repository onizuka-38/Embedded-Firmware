from __future__ import annotations

from pathlib import Path

from evaluate_inference_csv import evaluate_inference


def _write_inference(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write("timestamp_ms,probability,label\n")
        handle.write("0,0.10,0\n")
        handle.write("100,0.20,0\n")
        handle.write("200,0.90,1\n")
        handle.write("300,0.80,1\n")
        handle.write("400,0.60,1\n")


def _write_intervals(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write("start_ms,end_ms,true_label\n")
        handle.write("0,199,0\n")
        handle.write("200,500,1\n")


def test_evaluate_inference(tmp_path: Path) -> None:
    inf_path = tmp_path / "inference.csv"
    int_path = tmp_path / "intervals.csv"

    _write_inference(inf_path)
    _write_intervals(int_path)

    metrics = evaluate_inference(inference_csv=inf_path, interval_csv=int_path, threshold=0.5)

    assert metrics.total == 5
    assert metrics.accuracy == 1.0
    assert metrics.precision == 1.0
    assert metrics.recall == 1.0
    assert metrics.f1 == 1.0


def test_evaluate_inference_threshold_effect(tmp_path: Path) -> None:
    inf_path = tmp_path / "inference.csv"
    int_path = tmp_path / "intervals.csv"

    _write_inference(inf_path)
    _write_intervals(int_path)

    metrics = evaluate_inference(inference_csv=inf_path, interval_csv=int_path, threshold=0.85)
    assert metrics.total == 5
    assert metrics.accuracy < 1.0
