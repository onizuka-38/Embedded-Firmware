# Execution Plan

1. RTOS bring-up
- Task skeletons, queues, and timing hooks
- Verify: all tasks alive + no stack overflow

2. IO integration
- PWM output + encoder counter read
- Verify: commanded duty reflects on scope

3. Control loop
- PID update at fixed period
- Verify: step response and overshoot targets

4. UART operations
- Runtime gain tuning and state telemetry
- Verify: command parser robustness
