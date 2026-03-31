# Rust Drone Flight Controller (no_std)

## Goal
Develop a memory-safe and deterministic flight controller on STM32 using Rust (`no_std`).

## Core Features
- IMU acquisition via SPI/I2C
- State estimation (attitude/gyro bias handling)
- PID-based attitude/rate control
- Motor mixing and output generation
- Telemetry and failsafe logic

## Framework Candidates
- `embassy` (async embedded)
- `rtic` (interrupt-driven concurrency)

Decision is documented in `docs/02_framework_decision.md`.
