# Execution Plan

1. CAN ingest
- Filter and parse required frame IDs
- Verify: parser tests for all IDs

2. State tracking
- SOC, voltage, current, min/max cell metrics
- Verify: deterministic state updates

3. Alarm logic
- Over/under thresholds and debounced warnings
- Verify: threshold crossing scenarios

4. Logging
- Rolling event log and telemetry output
- Verify: event ordering and recovery behavior
