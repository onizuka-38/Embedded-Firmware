from __future__ import annotations

from ble_payload_verify import encode_payload, verify_payload


def test_ble_payload_checksum() -> None:
    payload = encode_payload(1234, 2510, 4870, 123456)
    assert verify_payload(payload)


def test_ble_payload_detects_corruption() -> None:
    payload = bytearray(encode_payload(1234, 2510, 4870, 123456))
    payload[4] ^= 0x01
    assert not verify_payload(bytes(payload))
