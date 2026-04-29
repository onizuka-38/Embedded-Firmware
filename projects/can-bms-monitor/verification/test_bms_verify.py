from __future__ import annotations

from bms_verify import BmsState, update_from_frame


def test_warning_rules() -> None:
    state = BmsState()
    update_from_frame(state, 0x181, bytes([0x03, 0x84, 0x10, 0x70]))
    update_from_frame(state, 0x182, bytes([0x0A, 0x00, 0x1A, 0x00]))
    update_from_frame(state, 0x180, bytes([0x0E, 0x74, 0x01, 0x00]))

    assert state.warning_flags & 1
    assert state.warning_flags & 2
    assert state.warning_flags & 4


def test_signed_current_parsing() -> None:
    state = BmsState()
    update_from_frame(state, 0x180, bytes([0x0E, 0x74, 0xFF, 0x9C]))
    assert state.pack_ma < 0
