from __future__ import annotations

from pathlib import Path

from merge_captures import merge_capture_csvs


def _write_capture(path: Path, label: int, count: int) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write("signal,label\n")
        for idx in range(count):
            signal = (idx / 50.0) - 0.5
            handle.write(f"{signal:.6f},{label}\n")


def test_merge_capture_csvs(tmp_path: Path) -> None:
    _write_capture(tmp_path / "normal.csv", label=0, count=80)
    _write_capture(tmp_path / "anomaly.csv", label=1, count=90)

    output = tmp_path / "merged.csv"
    row_count = merge_capture_csvs(tmp_path, output, min_rows=100)

    content = output.read_text(encoding="utf-8")
    assert row_count == 170
    assert "signal,label" in content
    assert ",0" in content
    assert ",1" in content
