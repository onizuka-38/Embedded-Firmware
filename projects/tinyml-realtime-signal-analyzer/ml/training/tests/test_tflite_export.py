from __future__ import annotations

from pathlib import Path

from tinyml_signal_analyzer.tflite_export import write_tflite_c_array


def test_write_tflite_c_array(tmp_path: Path) -> None:
    tflite_path = tmp_path / "model.tflite"
    tflite_path.write_bytes(bytes([0x20, 0x00, 0x01, 0x7F]))

    header_path = tmp_path / "tinyml_model_data.h"
    source_path = tmp_path / "tinyml_model_data.c"

    write_tflite_c_array(
        tflite_path=tflite_path,
        header_path=header_path,
        source_path=source_path,
        symbol_name="g_tinyml_model_data",
    )

    header = header_path.read_text(encoding="utf-8")
    source = source_path.read_text(encoding="utf-8")

    assert "extern const unsigned char g_tinyml_model_data[];" in header
    assert "0x20, 0x00, 0x01, 0x7f" in source
