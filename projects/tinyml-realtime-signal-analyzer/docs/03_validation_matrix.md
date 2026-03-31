# Validation Matrix

## Functional
- F-01 Sensor stream continuity
- F-02 Correct window segmentation
- F-03 Stable inference output under static input

## Performance
- P-01 Inference latency per window
- P-02 Peak RAM (tensor arena + buffers)
- P-03 CPU utilization in steady state

## Reliability
- R-01 30-minute continuous run without fault
- R-02 Graceful handling of sensor disconnect/reconnect

## Deliverables
- Benchmark log CSV
- On-target console logs
- Validation summary report
