# Execution Plan

## Success Criteria
- End-to-end inference loop runs on target STM32 board.
- Windowed signal classification latency <= 50 ms per inference (initial target).
- Biomedical or industrial demo scenario achieves agreed baseline metrics.

## Phase Plan
1. Phase 1 - Scope and requirements
- Define sampling rate, window length, classes, deployment constraints.
- Verify: requirement checklist approved.

2. Phase 2 - Data acquisition and labeling
- Implement raw capture firmware and host-side logging script.
- Verify: at least 1 hour of labeled signal data collected.

3. Phase 3 - Model training and compression
- Train baseline model, then quantize to int8 for TFLM.
- Verify: offline validation report (`accuracy`, `f1`, confusion matrix).

4. Phase 4 - Firmware integration
- Integrate model C array, preprocessing pipeline, inference scheduler.
- Verify: model boots and emits stable class outputs over UART.

5. Phase 5 - Optimization and reliability
- Tune arena size, CPU load, and memory footprint.
- Verify: no memory overflow, no realtime deadline miss in 30-minute run.

6. Phase 6 - Demo and documentation
- Prepare repeatable demo scripts (biomedical or industrial).
- Verify: demo checklist and reproduction steps complete.
