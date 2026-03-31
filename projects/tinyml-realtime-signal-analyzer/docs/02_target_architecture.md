# Target Architecture

## Firmware Flow
1. Sensor ISR/driver sampling
2. Ring buffer accumulation
3. Window extraction + preprocessing (normalize/filter)
4. TFLM inference
5. Post-processing (threshold/smoothing)
6. Telemetry output (UART/USB)

## Modules
- `firmware/Core`: boot, main loop, scheduler hooks
- `firmware/Config`: sample rates, window sizes, class map
- `firmware/Middlewares/tflm`: TFLM sources and adapters
- `firmware/Tests`: unit-like tests on host/target stubs
- `ml/`: dataset, training, quantization, export scripts
- `hardware/`: wiring/schematic/BOM
