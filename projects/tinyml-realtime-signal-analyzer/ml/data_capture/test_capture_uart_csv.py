from __future__ import annotations

from capture_uart_csv import _parse_raw_line


def test_parse_raw_line() -> None:
    assert _parse_raw_line("RAW,0.123000") == 0.123
    assert _parse_raw_line("INF,0.81,1") is None
    assert _parse_raw_line("RAW,abc") is None
    assert _parse_raw_line("RAW") is None
