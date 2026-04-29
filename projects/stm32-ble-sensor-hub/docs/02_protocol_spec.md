# BLE Payload Spec

Byte layout (`BLE_PAYLOAD_BYTES = 12`):
- 0: magic `0xA5`
- 1..2: `adc_mv` big-endian
- 3..4: `temp_centi` signed big-endian
- 5..6: `humidity_centi` signed big-endian
- 7..10: `timestamp_ms` big-endian
- 11: xor checksum of bytes 0..10
