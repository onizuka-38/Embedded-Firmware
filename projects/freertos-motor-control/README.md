# FreeRTOS Motor Control

## Scope
- PID with anti-windup
- Runtime target/feedback update path
- Safety flags for invalid timing and feedback range

## Firmware Quality Points
- Output saturation + integral rollback
- Deterministic control step API (`motor_control_step`)
- Explicit fault bit tracking

## Verification Checklist
1. Positive step command produces positive duty within [0,1].
2. Invalid `dt_s` sets `MOTOR_FAULT_INVALID_DT`.
3. Out-of-range feedback sets `MOTOR_FAULT_SPEED_RANGE`.
