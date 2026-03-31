from __future__ import annotations

import argparse
import csv
from pathlib import Path


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--min-rows", type=int, default=100)
    return parser.parse_args()


def _read_rows(path: Path) -> list[tuple[float, int]]:
    rows: list[tuple[float, int]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        required = {"signal", "label"}
        if not required.issubset(set(fieldnames)):
            raise ValueError(f"{path}: missing required columns signal,label")

        for row in reader:
            rows.append((float(row["signal"]), int(row["label"])))

    return rows


def merge_capture_csvs(input_dir: Path, output_path: Path, min_rows: int) -> int:
    if min_rows <= 0:
        raise ValueError("min_rows must be positive")
    if not input_dir.exists():
        raise ValueError(f"input directory not found: {input_dir}")

    input_files = sorted(input_dir.glob("*.csv"))
    if not input_files:
        raise ValueError(f"no csv files found in {input_dir}")

    merged: list[tuple[float, int]] = []
    for csv_path in input_files:
        merged.extend(_read_rows(csv_path))

    if len(merged) < min_rows:
        raise ValueError(f"not enough rows: {len(merged)} < {min_rows}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["signal", "label"])
        for signal, label in merged:
            writer.writerow([f"{signal:.6f}", label])

    return len(merged)


def main() -> None:
    args = _parse_args()
    row_count = merge_capture_csvs(args.input_dir, args.output, args.min_rows)
    print(f"merged_rows={row_count}")


if __name__ == "__main__":
    main()
