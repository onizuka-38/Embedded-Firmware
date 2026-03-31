from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TRAINING_SRC = PROJECT_ROOT / "ml" / "training" / "src"
sys.path.insert(0, str(TRAINING_SRC))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=PROJECT_ROOT / "ml" / "data" / "raw",
    )
    parser.add_argument("--window-size", type=int, default=128)
    parser.add_argument("--stride", type=int, default=32)
    return parser.parse_args()


def main() -> None:
    from tinyml_signal_analyzer.pipeline import export_model_header, run_training_pipeline

    args = _parse_args()
    artifact = run_training_pipeline(
        dataset_dir=args.dataset_dir,
        window_size=args.window_size,
        stride=args.stride,
        seed=42,
    )
    output = PROJECT_ROOT / "firmware" / "Config" / "tinyml_model_params.h"
    export_model_header(artifact, output)


if __name__ == "__main__":
    main()
