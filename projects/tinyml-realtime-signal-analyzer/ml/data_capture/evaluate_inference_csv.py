from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class IntervalLabel:
    start_ms: int
    end_ms: int
    true_label: int


@dataclass(frozen=True)
class Metrics:
    total: int
    accuracy: float
    precision: float
    recall: float
    f1: float


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inference-csv", type=Path, required=True)
    parser.add_argument("--interval-csv", type=Path, required=True)
    parser.add_argument("--threshold", type=float, default=0.5)
    return parser.parse_args()


def _load_intervals(path: Path) -> list[IntervalLabel]:
    intervals: list[IntervalLabel] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"start_ms", "end_ms", "true_label"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError("interval CSV must contain start_ms,end_ms,true_label columns")

        for row in reader:
            start_ms = int(row["start_ms"])
            end_ms = int(row["end_ms"])
            true_label = int(row["true_label"])
            if end_ms < start_ms:
                raise ValueError("interval end_ms must be >= start_ms")
            intervals.append(IntervalLabel(start_ms=start_ms, end_ms=end_ms, true_label=true_label))

    if not intervals:
        raise ValueError("interval CSV must contain at least one row")

    return sorted(intervals, key=lambda item: item.start_ms)


def _true_label_for_timestamp(timestamp_ms: int, intervals: list[IntervalLabel]) -> int | None:
    for item in intervals:
        if item.start_ms <= timestamp_ms <= item.end_ms:
            return item.true_label
    return None


def evaluate_inference(
    inference_csv: Path,
    interval_csv: Path,
    threshold: float,
) -> Metrics:
    if threshold < 0.0 or threshold > 1.0:
        raise ValueError("threshold must be in range [0, 1]")

    intervals = _load_intervals(interval_csv)

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    with inference_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"timestamp_ms", "probability", "label"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError("inference CSV must contain timestamp_ms,probability,label columns")

        for row in reader:
            timestamp_ms = int(row["timestamp_ms"])
            probability = float(row["probability"])
            pred_label = 1 if probability >= threshold else 0

            true_label = _true_label_for_timestamp(timestamp_ms, intervals)
            if true_label is None:
                continue

            if pred_label == 1 and true_label == 1:
                tp += 1
            elif pred_label == 0 and true_label == 0:
                tn += 1
            elif pred_label == 1 and true_label == 0:
                fp += 1
            else:
                fn += 1

    total = tp + tn + fp + fn
    if total == 0:
        raise ValueError("no overlapping rows between inference and interval labels")

    accuracy = (tp + tn) / float(total)
    precision = tp / float(tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / float(tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2.0 * precision * recall / (precision + recall)) if (precision + recall) > 0.0 else 0.0

    return Metrics(total=total, accuracy=accuracy, precision=precision, recall=recall, f1=f1)


def main() -> None:
    args = _parse_args()
    metrics = evaluate_inference(
        inference_csv=args.inference_csv,
        interval_csv=args.interval_csv,
        threshold=args.threshold,
    )

    print(f"total={metrics.total}")
    print(f"accuracy={metrics.accuracy:.6f}")
    print(f"precision={metrics.precision:.6f}")
    print(f"recall={metrics.recall:.6f}")
    print(f"f1={metrics.f1:.6f}")


if __name__ == "__main__":
    main()
