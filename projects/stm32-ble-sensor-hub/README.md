# STM32 BLE Sensor Hub

## Scope
- Sensor acquisition with stale-data fallback
- BLE payload encoding with checksum
- Clear port abstraction for board-specific IO

## Firmware Quality Points
- Moving-average filtering for noisy ADC
- Sensor timeout handling (`SENSOR_STATUS_STALE`)
- Fixed-size payload contract (`BLE_PAYLOAD_BYTES`)

## Verification Checklist
1. Sensor read failure keeps last valid sample only within stale window.
2. BLE payload checksum matches XOR of bytes [0..10].
3. Payload fields decode to original engineering values.
