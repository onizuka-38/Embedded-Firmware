# TinyML Realtime Signal Analyzer (STM32 + TFLM)

## Goal
Run lightweight deep learning inference on STM32 in realtime for biomedical and industrial signal classification.

## Current Implementation Status
- `.ioc` target scaffold for STM32CubeIDE exists.
- TFLM `MicroInterpreter` runtime path is wired (`tinyml_inference.cc`).
- Feature pipeline runs on target path: raw sample -> ring buffer -> feature extraction -> normalization -> inference.
- Telemetry supports two line formats:
  - `RAW,<sample>` for data collection mode
  - `INF,<probability>,<label>` for inference mode
- Python pipeline supports:
  - measurement CSV loader (`signal,label`)
  - training + header export
  - optional `.tflite` to `tinyml_model_data.c/.h` conversion

## Folder Layout
- `firmware/Core`: runtime logic and adapters
- `firmware/Config`: generated model params and TFLite C array
- `firmware/Scripts`: helper scripts for capture/export
- `ml/data_capture`: UART capture and dataset merge tools
- `ml/training`: training and quantization pipeline
- `ml/export`: model export entrypoint

## Quick Start
1. Build raw capture firmware mode
- Set `TINYML_CAPTURE_RAW_STREAM` to `1` in `firmware/Core/Inc/tinyml_app_config.h`.
- Flash and run board.

2. Capture labeled data
- Run:
```powershell
powershell -ExecutionPolicy Bypass -File projects/tinyml-realtime-signal-analyzer/firmware/Scripts/capture_and_build_dataset.ps1 -Port COM5
```

3. Train and export params/TFLite array
- Run:
```powershell
python projects/tinyml-realtime-signal-analyzer/ml/export/export_model.py `
  --dataset-dir projects/tinyml-realtime-signal-analyzer/ml/data/raw `
  --window-size 128 --stride 32 `
  --tflite-path C:\path\to\model.tflite
```

4. Build inference firmware mode
- Set `TINYML_CAPTURE_RAW_STREAM` back to `0`.
- Add files listed in `firmware/Scripts/cubeide_required_sources.txt` to CubeIDE build.
- Flash and monitor `INF,<probability>,<label>` telemetry.

## Notes
- `sensor_port_stub.c` / `telemetry_port_stub.c` are fallback stubs.
- For real board IO, enable and wire STM32-specific ports (`sensor_port_stm32_adc.c`, `telemetry_port_stm32_uart.c`).
