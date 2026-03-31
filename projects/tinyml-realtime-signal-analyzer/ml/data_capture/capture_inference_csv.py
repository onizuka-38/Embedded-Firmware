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
        default=Path("projects/tinyml-realtime-signal-analyzer/ml/data/raw/inference_log.csv"),
    )
    return parser.parse_args()


def _parse_inf_line(line: str) -> tuple[float, int] | None:
    # Expected firmware format: INF,<probability>,<label>
    parts = line.split(",")
    if len(parts) != 3:
        return None
    if parts[0] != "INF":
        return None

    try:
        probability = float(parts[1])
        label = int(parts[2])
    except ValueError:
        return None

    return probability, label


def main() -> None:
    try:
        import serial
    except ModuleNotFoundError as exc:
        raise SystemExit("pyserial is required: pip install pyserial") from exc

    args = _parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    start = time.time()
    end_time = start + float(args.seconds)

    with serial.Serial(args.port, args.baud, timeout=1.0) as ser, args.output.open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(["timestamp_ms", "probability", "label"])

        while time.time() < end_time:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if not line:
                continue

            parsed = _parse_inf_line(line)
            if parsed is None:
                continue

            probability, label = parsed
            timestamp_ms = int((time.time() - start) * 1000.0)
            writer.writerow([timestamp_ms, f"{probability:.6f}", label])


if __name__ == "__main__":
    main()
