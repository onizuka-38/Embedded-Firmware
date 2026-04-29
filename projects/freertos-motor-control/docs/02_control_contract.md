# Control Contract

- `motor_control_step(dt_s)` expects fixed-period call.
- Duty output range: `[0.0, 1.0]`.
- Fault flags:
  - bit0: invalid `dt_s`
  - bit1: feedback out-of-range
