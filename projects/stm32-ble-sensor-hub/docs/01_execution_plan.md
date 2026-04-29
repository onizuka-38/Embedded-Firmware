# Execution Plan

1. Platform bring-up
- Clock, GPIO, ADC/I2C/UART init
- Verify: boot log + stable sensor read

2. BLE transport
- Advertising packet format and update loop
- Verify: mobile scanner sees live values

3. Power profile
- Sleep/wake schedule and periodic publish
- Verify: average current within target

4. Reliability
- Sensor timeout handling + stale-data marking
- Verify: fault injection tests pass
