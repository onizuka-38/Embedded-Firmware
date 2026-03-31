# Module Architecture

## Firmware Layout
- `firmware/fc-rs/src/main.rs`: startup and task graph
- `firmware/drivers/`: IMU, baro, receiver, PWM abstractions
- `firmware/estimator/`: attitude/heading estimation
- `firmware/control/`: PID loops and mixer
- `firmware/comms/`: telemetry, CLI, config protocol
- `firmware/tests/`: host-based algorithm tests

## Data Flow
1. Read sensors
2. Estimate state
3. Compute control outputs
4. Mix to motors
5. Publish telemetry
