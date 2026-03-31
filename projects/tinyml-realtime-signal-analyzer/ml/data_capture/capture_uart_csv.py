from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", required=True)
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--seconds", type=int, default=60)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("projects/tinyml-realtime-signal-analyzer/ml/data/raw/capture.csv"),
    )
    parser.add_argument("--label", type=int, required=True)
    return parser.parse_args()


def main() -> None:
    try:
        import serial  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        raise SystemExit("pyserial is required: pip install pyserial") from exc

    args = _parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    end_time = time.time() + float(args.seconds)
    with serial.Serial(args.port, args.baud, timeout=1.0) as ser, args.output.open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(["signal", "label"])

        while time.time() < end_time:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if not line:
                continue
            try:
                sample = float(line)
            except ValueError:
                continue
            writer.writerow([f"{sample:.6f}", args.label])


if __name__ == "__main__":
    main()
