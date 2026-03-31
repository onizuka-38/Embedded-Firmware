from __future__ import annotations

from pathlib import Path


def _format_c_array(data: bytes, bytes_per_line: int = 12) -> str:
    if bytes_per_line <= 0:
        raise ValueError("bytes_per_line must be positive")

    chunks: list[str] = []
    for start in range(0, len(data), bytes_per_line):
        part = data[start : start + bytes_per_line]
        chunks.append(", ".join(f"0x{value:02x}" for value in part))
    return ",\n    ".join(chunks)


def write_tflite_c_array(
    tflite_path: Path,
    header_path: Path,
    source_path: Path,
    symbol_name: str = "g_tinyml_model_data",
) -> None:
    if not tflite_path.exists():
        raise ValueError(f"tflite model file not found: {tflite_path}")
    if not symbol_name.isidentifier():
        raise ValueError("symbol_name must be a valid C identifier")

    model_bytes = tflite_path.read_bytes()
    if len(model_bytes) == 0:
        raise ValueError("tflite model file is empty")

    guard = f"{symbol_name.upper()}_H"
    header_lines = [
        f"#ifndef {guard}",
        f"#define {guard}",
        "",
        "#include <stdint.h>",
        "",
        f"extern const unsigned char {symbol_name}[];",
        f"extern const unsigned int {symbol_name}_len;",
        "",
        "#endif",
    ]

    array_body = _format_c_array(model_bytes)
    source_lines = [
        f"#include \"{header_path.name}\"",
        "",
        f"const unsigned char {symbol_name}[] = {{",
        f"    {array_body}",
        "};",
        f"const unsigned int {symbol_name}_len = sizeof({symbol_name});",
    ]

    header_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.parent.mkdir(parents=True, exist_ok=True)
    header_path.write_text("\n".join(header_lines) + "\n", encoding="utf-8")
    source_path.write_text("\n".join(source_lines) + "\n", encoding="utf-8")
