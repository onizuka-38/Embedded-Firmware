from __future__ import annotations

from capture_inference_csv import _parse_inf_line


def test_parse_inf_line() -> None:
    assert _parse_inf_line("INF,0.81234,1") == (0.81234, 1)
    assert _parse_inf_line("RAW,0.12") is None
    assert _parse_inf_line("INF,abc,1") is None
    assert _parse_inf_line("INF,0.3,a") is None
    assert _parse_inf_line("INF,0.3") is None
