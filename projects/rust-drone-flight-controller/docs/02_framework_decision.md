# Framework Decision Template

## Option A: embassy
Pros
- Async model simplifies peripheral orchestration.
- Good ecosystem momentum for modern embedded Rust.

Cons
- Async mental model complexity for strict control-loop timing.

## Option B: rtic
Pros
- Strong interrupt-priority model for deterministic scheduling.
- Clear mapping to control-loop periodic tasks.

Cons
- Some patterns can be more verbose for background services.

## Decision Rule
- If deterministic fixed-rate control simplicity is highest priority: prefer RTIC.
- If mixed IO workloads and integration flexibility dominate: prefer embassy.

## Current Status
- Pending board and timing budget selection.
