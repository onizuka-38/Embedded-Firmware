from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TRAINING_SRC = PROJECT_ROOT / "ml" / "training" / "src"
sys.path.insert(0, str(TRAINING_SRC))


def main() -> None:
    from tinyml_signal_analyzer.pipeline import export_model_header, run_training_pipeline

    artifact = run_training_pipeline(window_size=128, sample_count=600, seed=42)
    output = PROJECT_ROOT / "firmware" / "Config" / "tinyml_model_params.h"
    export_model_header(artifact, output)


if __name__ == "__main__":
    main()
