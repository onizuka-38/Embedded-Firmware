from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BmsState:
    pack_mv: int = 0
    pack_ma: int = 0
    soc_tenths: int = 0
    max_cell_mv: int = 0
    min_cell_mv: int = 0
    max_temp_centi: int = 0
    min_temp_centi: int = 0
    warning_flags: int = 0


def u16be(data: bytes, idx: int) -> int:
    return (data[idx] << 8) | data[idx + 1]


def s16be(data: bytes, idx: int) -> int:
    value = u16be(data, idx)
    return value - 65536 if value >= 32768 else value


def apply_rules(state: BmsState) -> None:
    flags = 0
    if state.max_cell_mv > 4200:
        flags |= 1
    if state.min_cell_mv > 0 and state.min_cell_mv < 2900:
        flags |= 2
    if state.max_temp_centi > 6500:
        flags |= 4
    if state.pack_ma > 120000 or state.pack_ma < -120000:
        flags |= 8
    state.warning_flags = flags


def update_from_frame(state: BmsState, can_id: int, data: bytes) -> None:
    if len(data) < 4:
        return
    if can_id == 0x180:
        state.pack_mv = u16be(data, 0)
        state.pack_ma = s16be(data, 2)
    elif can_id == 0x181:
        state.soc_tenths = u16be(data, 0)
        state.max_cell_mv = u16be(data, 2)
    elif can_id == 0x182:
        state.min_cell_mv = u16be(data, 0)
        state.max_temp_centi = s16be(data, 2)
    elif can_id == 0x183:
        state.min_temp_centi = s16be(data, 0)

    apply_rules(state)
