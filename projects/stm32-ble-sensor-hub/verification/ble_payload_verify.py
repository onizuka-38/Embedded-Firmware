from __future__ import annotations


def encode_payload(adc_mv: int, temp_centi: int, humidity_centi: int, timestamp_ms: int) -> bytes:
    raw = bytearray(12)
    raw[0] = 0xA5
    raw[1] = (adc_mv >> 8) & 0xFF
    raw[2] = adc_mv & 0xFF
    raw[3] = (temp_centi >> 8) & 0xFF
    raw[4] = temp_centi & 0xFF
    raw[5] = (humidity_centi >> 8) & 0xFF
    raw[6] = humidity_centi & 0xFF
    raw[7] = (timestamp_ms >> 24) & 0xFF
    raw[8] = (timestamp_ms >> 16) & 0xFF
    raw[9] = (timestamp_ms >> 8) & 0xFF
    raw[10] = timestamp_ms & 0xFF

    checksum = 0
    for i in range(11):
        checksum ^= raw[i]
    raw[11] = checksum
    return bytes(raw)


def verify_payload(payload: bytes) -> bool:
    if len(payload) != 12:
        return False
    if payload[0] != 0xA5:
        return False
    checksum = 0
    for i in range(11):
        checksum ^= payload[i]
    return checksum == payload[11]
